import os
import json
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
from .sub_agent import SubAgent
from colorama import Fore, Style

load_dotenv()

class OrchestratorAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def decide_mode(self, user_input):
        system_prompt = (
            "You are an orchestrator agent. Classify the input:\n"
            "1. 'DIRECT': Simple questions, greetings.\n"
            "2. 'PLAN': Complex tasks, multi-step requests.\n"
            "Respond ONLY with 'DIRECT' or 'PLAN'."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
            )
            mode = response.choices[0].message.content.strip().upper()
            return "PLAN" if "PLAN" in mode else "DIRECT"
        except Exception:
            return "DIRECT"

    def generate_response(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer directly."},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def generate_plan(self, user_input):
        """Generates a JSON plan with pre-calculated complexity."""
        system_prompt = (
            "You are a strategic planner. Break the user's request into logical steps.\n"
            "For EACH step, determine if it is 'SIMPLE' (general knowledge) or 'COMPLEX' (coding, research, specific generation).\n"
            "Return a JSON object with a key 'steps'.\n"
            "Each item in 'steps' must be an object: {\"instruction\": \"...\", \"complexity\": \"SIMPLE\" or \"COMPLEX\"}\n"
            "Example: {\"steps\": [{\"instruction\": \"Define concept\", \"complexity\": \"SIMPLE\"}, {\"instruction\": \"Write code\", \"complexity\": \"COMPLEX\"}]}\n"
            "Ensure the output is VALID JSON."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"}, 
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
            )
            content = response.choices[0].message.content
            content = re.sub(r"```json|```", "", content).strip()
            return json.loads(content)
        except Exception as e:
            print(f"{Fore.RED}Plan generation error: {e}{Style.RESET_ALL}")
            return None

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
                step_result = self.generate_response(f"Context: {overall_context}\nTask: {instruction}")
            else:
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
        print(f"{Fore.CYAN}Analyzing request...{Style.RESET_ALL}", end="\r")
        mode = self.decide_mode(user_input)
        
        if mode == "PLAN":
            print(f"{Fore.CYAN}Mode: {Fore.YELLOW}PLANNING{Style.RESET_ALL}                                 ")
            if callback: await callback({"type": "mode", "mode": "PLAN"})
            
            plan = self.generate_plan(user_input)
            if plan:
                return await self.execute_plan(plan, user_input, callback)
            else:
                return "Failed to generate a valid plan."
        else:
            print(f"{Fore.CYAN}Mode: {Fore.GREEN}DIRECT{Style.RESET_ALL}                                   ")
            if callback: await callback({"type": "mode", "mode": "DIRECT"})
            
            response = self.generate_response(user_input)
            return response
