"""
OrchestratorAgent - Main agent that creates plans and orchestrates sub-agents.
"""

import os
import json
import traceback
from openai import OpenAI
from dotenv import load_dotenv
from typing import Callable, Optional, List, Dict, Any
from dataclasses import dataclass
from app.agents.sandbox import Sandbox, sandbox_manager
from app.tools.registry import ToolRegistry, ToolResult
from app.agents.chat_history import chat_history_manager
from app.agents.sub_agent import SubAgent, TaskDefinition, TaskResult
from app.agents.validator import TaskValidator, ValidationResult

load_dotenv()


@dataclass
class PlanStep:
    """A single step in the execution plan."""
    id: str
    objective: str
    context: str = ""
    status: str = "pending"  # pending, executing, validating, completed, failed


class OrchestratorAgent:
    """
    Main orchestrator agent that creates plans and supervises sub-agents.
    Uses a multi-agent architecture with validation.
    """

    SYSTEM_PROMPT = """You are a versatile AI assistant.

Use your tools to accomplish whatever the user asks. Be concise and natural.

CORE PRINCIPLES:
1. Understand the request - What does the user actually want?
2. Plan dynamically - Figure out the best approach
3. Execute proactively - Don't just explain, DO the work
4. Adapt and iterate - If something fails, debug and fix it
5. Be thorough - Complete the task fully

Never introduce yourself, all u know is that u was created by hatim in 2026."""

    PLANNER_PROMPT = """You are a task planner. Break down the user's request into sequential steps.

Each step should be:
- Specific and actionable
- Independent but may build on previous steps
- Achievable using available tools (write_file, terminal, etc.)
- If the user provides code, Step 1 MUST be to write that code to a file, and Step 2 to execute it.

Respond with a JSON array of steps:
[
  {
    "id": "step_1",
    "objective": "Create main.py with basic structure",
    "context": "Use the code provided by the user if available"
  },
  {
    "id": "step_2", 
    "objective": "Test the script by running it",
    "context": "After step_1 creates the file"
  }
]

Keep it CONCISE. Maximum 5-7 steps. Be practical.

IMPORTANT:
- If the user provides a script (Python, JS, etc.), YOU MUST Plan to:
  1. Write the file (e.g. 'write_file main.py')
  2. Execute the file (e.g. 'terminal python main.py')
- Do NOT assume the file exists. Always write it first."""

    def __init__(self, project_id: Optional[str] = None):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3")

        if self.api_key:
            self.api_key = self.api_key.strip()

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "Agent Workspace",
            }
        )

        # Initialize sandbox and tools for the project
        self.project_id = project_id
        self.sandbox: Optional[Sandbox] = None
        self.tools: Optional[ToolRegistry] = None
        self.validator: Optional[TaskValidator] = None

        if project_id:
            self.set_project(project_id)

        # Conversation history
        self.messages = []
        
        # Current execution plan
        self.current_plan: List[PlanStep] = []

    def set_project(self, project_id: str):
        """Set the current project and initialize its sandbox."""
        self.project_id = project_id
        self.sandbox = sandbox_manager.get_or_create(project_id)
        self.tools = ToolRegistry(self.sandbox)
        self.validator = TaskValidator(self.client, self.model)
        # Load chat history for this project
        self.messages = chat_history_manager.load(project_id)

    async def run(
        self,
        user_input: str,
        callback: Optional[Callable] = None
    ) -> str:
        """
        Process user input using multi-agent architecture.

        Args:
            user_input: The user's message
            callback: Optional callback for streaming events to the client

        Returns:
            The final response text
        """
        if not self.project_id or not self.sandbox or not self.tools:
            return "Error: No project selected. Please select or create a project first."

        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})

        try:
            # 1. Check if this needs a plan or is just a simple query
            needs_execution = await self._needs_execution(user_input)
            
            if not needs_execution:
                # Simple query - respond directly
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        *self.messages
                    ]
                )
                final_content = response.choices[0].message.content
            else:
                # Complex task - use multi-agent workflow
                final_content = await self._execute_multi_agent_workflow(user_input, callback)

            # Add final response to history
            self.messages.append({
                "role": "assistant",
                "content": final_content
            })

            # Save chat history
            if self.project_id:
                chat_history_manager.save(self.project_id, self.messages)

            return final_content

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Agent error: {e}")
            traceback.print_exc()
            
            if callback:
                await callback({"type": "error", "content": error_msg})
            
            return error_msg

    async def _needs_execution(self, user_input: str) -> bool:
        """
        Use LLM to decide if the request needs a plan or is just immediate conversation.
        This implements the 'Analyze First' requirement.
        """
        prompt = f"""Analyze this user request:
"{user_input}"

Does this request require:
A) IMMEDIATE RESPONSE (simple questions, explanations, greetings, translations, standard chat)
B) EXECUTION PLAN (writing code, creating files, running commands, multi-step tasks, fixing bugs)

If the user provides code and asks to "run" or "test" or "implement" it, choose B.
If the user asks to create a file or PDF, choose B.

Reply with ONLY 'A' or 'B'.
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            decision = response.choices[0].message.content.strip().upper()
            return "B" in decision
        except:
            # Fallback to keyword heuristics if LLM fails
            action_keywords = ["crée", "exécute", "lance", "write", "run", "code"]
            return any(k in user_input.lower() for k in action_keywords)

    async def _execute_multi_agent_workflow(
        self,
        user_input: str,
        callback: Optional[Callable]
    ) -> str:
        """Execute the multi-agent workflow with planning and validation."""
        
        # Step 1: Generate plan
        if callback:
            await callback({"type": "status", "status": "planning", "message": "Creating execution plan..."})
        
        plan = await self._generate_plan(user_input)
        self.current_plan = plan
        
        if callback:
            await callback({
                "type": "plan_created",
                "plan": [{"id": s.id, "objective": s.objective, "status": s.status} for s in plan]
            })
        
        # Step 2: Execute plan sequentially with validation
        results = []
        
        for i, step in enumerate(plan):
            step.status = "executing"
            
            if callback:
                await callback({
                    "type": "step_started",
                    "step_id": step.id,
                    "objective": step.objective,
                    "progress": f"{i+1}/{len(plan)}"
                })
            
            # Create and execute sub-agent
            task_def = TaskDefinition(
                id=step.id,
                objective=step.objective,
                context=step.context + "\n\nPrevious results:\n" + "\n".join(results[-2:])
            )
            
            sub_agent = SubAgent(task_def, self.tools, self.client, self.model)
            task_result = await sub_agent.execute(callback)
            
            # Validate result
            step.status = "validating"
            
            if callback:
                await callback({"type": "step_validating", "step_id": step.id})
            
            validation = await self.validator.validate(
                task_objective=step.objective,
                task_result=task_result.__dict__,
                context={
                    "files_created": task_result.files_created,
                    "files_modified": task_result.files_modified,
                    "terminal_output": task_result.terminal_output
                }
            )
            
            # Check validation
            if validation.success and validation.confidence > 0.6:
                step.status = "completed"
                results.append(f"✓ {step.objective}: {task_result.output[:100]}")
                
                if callback:
                    await callback({
                        "type": "step_completed",
                        "step_id": step.id,
                        "validation": {"success": True, "feedback": validation.feedback}
                    })
            else:
                step.status = "failed"
                results.append(f"✗ {step.objective}: {validation.feedback}")
                
                if callback:
                    await callback({
                        "type": "step_failed",
                        "step_id": step.id,
                        "validation": {"success": False, "feedback": validation.feedback}
                    })
                
                # For now, continue despite failure (future: retry logic)
        
        # Step 3: Generate final summary
        summary = "Task completed. Results:\n" + "\n".join(results)
        return summary

    async def _generate_plan(self, user_input: str) -> List[PlanStep]:
        """Generate a structured execution plan."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.PLANNER_PROMPT},
                {"role": "user", "content": f"Create a plan for: {user_input}"}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        try:
            steps_data = json.loads(content)
            return [PlanStep(**step) for step in steps_data]
        except:
            # Fallback: single step plan
            return [PlanStep(
                id="step_1",
                objective=user_input,
                context="Execute the user's request directly"
            )]
