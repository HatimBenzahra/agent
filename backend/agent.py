import os
import json
import re
import time
import traceback
from openai import OpenAI
from dotenv import load_dotenv
from .sub_agent import SubAgent
from colorama import Fore, Style

load_dotenv()

class OrchestratorAgent:
    def __init__(self):
        # Explicitly load from root if needed, though no-arg load_dotenv() usually finds it in CWD
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
        
        # Debugging Auth
        if self.api_key:
            self.api_key = self.api_key.strip()
            
        masked_key = f"{self.api_key[:8]}...{self.api_key[-4:]}" if self.api_key else "None"
        print(f"{Fore.YELLOW}DEBUG: API Key Loaded: {masked_key}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}DEBUG: Model: {self.model}{Style.RESET_ALL}")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:5173", # Required for OpenRouter
                "X-Title": "Local Orchestrator Agent", # Required for OpenRouter
            }
        )

    async def orchestrate(self, user_input, callback=None):
        """
        Single-call architecture: Decides mode AND generates plan/response in one go.
        """
        system_prompt = (
            "You are an intelligent Orchestrator. Analyzes the user's request.\n"
            "1. IF the request is SIMPLE (greetings, quick questions), return a direct plain text response.\n"
            "2. IF the request is COMPLEX (requires coding, multi-step actions), return a JSON object with a 'steps' key.\n"
            "   - Format: {'steps': [{'instruction': '...', 'complexity': 'SIMPLE'|'COMPLEX'}]}\n"
            "   - Ensure it is VALID JSON."
        )

        try:
            # Notify analysis start
            if callback: await callback({"type": "log", "content": "Analyzing request..."})
            
            print(f"{Fore.YELLOW}DEBUG: calling LLM with input: {user_input}{Style.RESET_ALL}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
            )
            print(f"{Fore.YELLOW}DEBUG: LLM response received{Style.RESET_ALL}")
            content = response.choices[0].message.content.strip()
            print(f"{Fore.YELLOW}DEBUG: Content: {content[:50]}...{Style.RESET_ALL}")

            # Attempt to parse as JSON Plan
            try:
                # Cleanup potential markdown code blocks
                clean_content = re.sub(r"```json|```", "", content).strip()
                if clean_content.startswith("{") and "steps" in clean_content:
                    print(f"{Fore.YELLOW}DEBUG: Detected JSON plan{Style.RESET_ALL}")
                    plan_data = json.loads(clean_content)
                    return await self.execute_plan(plan_data, user_input, callback)
            except json.JSONDecodeError:
                pass # Not JSON, treat as direct response

            # If we get here, it's a direct response
            print(f"{Fore.YELLOW}DEBUG: Returning direct response{Style.RESET_ALL}")
            return content

        except Exception as e:
            print(f"{Fore.RED}DEBUG: Orchestrate Error: {e}{Style.RESET_ALL}")
            traceback.print_exc()
            return f"Error: {e}"

    async def execute_plan(self, plan_data, original_request, callback=None):
        """Executes the plan with optional callback for streaming updates."""
        steps = plan_data.get("steps", [])
        overall_context = f"Goal: {original_request}\n"

        # Notify Plan Start
        if callback:
            await callback({"type": "plan", "data": steps})

        # Visualization (CLI fallback)
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        
        # Execution Loop
        for i, step in enumerate(steps):
            instruction = step.get('instruction')
            complexity = step.get('complexity')
            
            # CLI Log
            print(f"{Fore.WHITE}Step {i+1}/{len(steps)}: {Style.BRIGHT}{instruction}{Style.RESET_ALL} ... ", end="", flush=True)

            # Callback Log
            if callback:
                await callback({
                    "type": "log", 
                    "step": i+1, 
                    "total": len(steps), 
                    "instruction": instruction,
                    "status": "started"
                })

            step_result = ""
            start_time = time.time()
            
            if complexity == "SIMPLE":
                # Brain does it
                # For sub-steps, we use a simple/fast prompt, no recursion for now
                try:
                    res = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are a helper. Execute this sub-task concisely."},
                            {"role": "user", "content": f"Context: {overall_context}\nTask: {instruction}"}
                        ]
                    )
                    step_result = res.choices[0].message.content
                except Exception as e:
                    step_result = f"Error: {e}"
            else:
                # Sub-Agent does it
                print(f"{Fore.MAGENTA}(Delegating to Sub-Agent){Style.RESET_ALL} ", end="", flush=True)
                if callback:
                     await callback({"type": "log", "content": f"Delegating '{instruction}' to Sub-Agent..."})
                
                sub_agent = SubAgent(role="Specialist", topic=instruction)
                step_result = sub_agent.run(instruction, context=overall_context)
            
            duration = time.time() - start_time
            print(f"{Fore.GREEN}Done ({duration:.1f}s){Style.RESET_ALL}")
            
            if callback:
                await callback({
                    "type": "log", 
                    "step": i+1, 
                    "instruction": instruction, 
                    "status": "completed", 
                    "duration": f"{duration:.1f}s",
                    "result": step_result
                })

            overall_context += f"\nResult of Step {i+1}: {step_result}\n"

        return overall_context

    async def run(self, user_input, callback=None):
        return await self.orchestrate(user_input, callback)
