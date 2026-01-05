"""
OrchestratorAgent - Main agent that creates plans and orchestrates sub-agents.
"""

import os
import json
import traceback
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import Callable, Optional, List, Dict, Any
from dataclasses import dataclass
from app.agents.sandbox import Sandbox, sandbox_manager
from app.tools.registry import ToolRegistry, ToolResult
from app.agents.chat_history import chat_history_manager
from app.agents.sub_agent import SubAgent, TaskDefinition, TaskResult
from app.agents.validator import TaskValidator, ValidationResult
from app.agents.context_manager import AdvancedContextManager
from app.agents.session_pipeline import SessionPipeline

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
- Focused on the GOAL
- Achievable using available tools

Respond with a JSON array of steps:
[
  {
    "id": "step_1",
    "objective": "Research/Check prerequisites",
    "context": "Gather info before acting"
  },
  {
    "id": "step_2", 
    "objective": "Execute core task",
    "context": "Use findings from step 1"
  }
]

Keep it CONCISE. Maximum 5-7 steps.
"""

    def __init__(self, project_id: Optional[str] = None):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3")

        if self.api_key:
            self.api_key = self.api_key.strip()

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        self.client = AsyncOpenAI(
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
        
        # Session pipeline for complete context tracking
        self.pipeline: Optional[SessionPipeline] = None

    def set_project(self, project_id: str):
        """Set the current project and initialize its sandbox."""
        self.project_id = project_id
        self.sandbox = sandbox_manager.get_or_create(project_id)
        self.tools = ToolRegistry(self.sandbox)
        self.validator = TaskValidator(self.client, self.model)
        # Load chat history for this project
        self.messages = chat_history_manager.load(project_id)
        # Initialize session pipeline
        self.pipeline = SessionPipeline(project_id, str(self.sandbox.workspace_path))

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
        
        # Log to pipeline
        if self.pipeline:
            self.pipeline.add_event("user_message", content=user_input)

        try:
            # 0. Retrieve Context (The "Brain" Upgrade)
            # Find relevant files and history dynamically
            context_mgr = AdvancedContextManager(self.client, self.model, self.sandbox, self.project_id) if self.project_id else None
            retrieved_context = await context_mgr.retrieve_context(user_input, self.messages, self.pipeline) if context_mgr else None
            
            # Augment user input with retrieved context for the agent's internal reasoning
            augmented_input = user_input
            if retrieved_context and retrieved_context.files:
                augmented_input += "\n\n[CONTEXT RETRIEVED FROM FILES]\n"
                for f in retrieved_context.files:
                    augmented_input += f"--- {f['path']} ---\n{f['content']}\n"
            
            # 1. Check if this needs a plan or is just a simple query
            # Pass the augmented input so it "knows" about the files
            intent = await self._needs_execution(augmented_input)
            
            if intent == "CLARIFY":
                # Ask user for clarification
                final_content = "Do you want me to just **show you the code** (Chat) or **implement it** in the workspace (Execute)? Reply with 'Show' or 'Implement'."
            elif intent == "RESPOND":
                # Simple query - respond directly
                # We inject context into system prompt or just append to messages temporarily
                messages_with_context = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    *self.messages[:-1], # History
                    {"role": "user", "content": augmented_input} # Augmented current message
                ]
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages_with_context
                )
                final_content = response.choices[0].message.content
            else: # EXECUTE
                # Complex task - use multi-agent workflow
                # The planner will now see the file content in 'augmented_input'
                final_content = await self._execute_multi_agent_workflow(augmented_input, callback)

            # Add final response to history
            self.messages.append({
                "role": "assistant",
                "content": final_content
            })
            
            # Log assistant response to pipeline
            if self.pipeline:
                self.pipeline.add_event(
                    "assistant_response",
                    content=final_content[:200]  # Truncate for storage
                )

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

    async def _needs_execution(self, user_input: str) -> str:
        """
        Use LLM to decide if the request needs a plan or is just immediate conversation.
        """
        # Get recent history (last 2 messages before the current one) to understand context
        # self.messages already includes the current user message at the end
        recent_history = self.messages[-5:-1] if len(self.messages) > 1 else []
        history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in recent_history])

        prompt = f"""Analyze the user's INTENT based on the conversation context.

RECENT CONVERSATION:
{history_text}

CURRENT USER REQUEST:
"{user_input}"

Classify the user's intent into one of these 3 categories:

A) IMMEDIATE RESPONSE (Chat / Explanation / Refusal)
- User wants to chat, ask a question, get an explanation, or see code WITHOUT execution.
- User replies "Show", "Display", "Just text", "Non", "Don't run" to a clarification question ou bien tu comprends d'apres la phrase que l utilisateur veut une simple reponse.
- User greeting or simple query.

B) EXECUTION (Implementation / Action / Confirmation)
- User wants to APPLY changes, CREATE files, RUN code, FIX bugs.
- User replies "Yes", "Do it", "Implement", "Go ahead", "Vas-y", "Fais-le" to a clarification question tu dois comprendre si c'est yes d'apres la phrase.
- User explicitly asks to "execute", "write file", "test".

C) CLARIFICATION (Ambiguity)
- The request is vague (e.g., "python script") AND there is NO prior context to clarify it.
- If the user is ANSWERING a previous clarification question, DO NOT choose C. Choose A or B based on their answer.

Reply with ONLY 'A', 'B', or 'C'.
"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            decision = response.choices[0].message.content.strip().upper()
            
            if "C" in decision:
                return "CLARIFY"
            elif "B" in decision:
                return "EXECUTE"
            else:
                return "RESPOND"
        except:
            # Fallback to keyword heuristics if LLM fails
            action_keywords = ["crée", "exécute", "lance", "write", "run", "code"]
            if any(k in user_input.lower() for k in action_keywords):
                return "EXECUTE"
            return "RESPOND"

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
        
        # Log plan to pipeline
        if self.pipeline:
            self.pipeline.add_event(
                "plan_generated",
                plan=[{"id": s.id, "objective": s.objective} for s in plan]
            )
        
        if callback:
            await callback({
                "type": "plan_created",
                "plan": [{"id": s.id, "objective": s.objective, "status": s.status} for s in plan]
            })
        
        # Step 2: Execute plan sequentially with validation
        results = []
        
        # Save initial plan state
        self._save_plan_state()
        
        for i, step in enumerate(plan):
            step.status = "executing"
            self._save_plan_state() # Save executing status
            
            if callback:
                await callback({
                    "type": "step_started",
                    "step_id": step.id,
                    "objective": step.objective,
                    "progress": f"{i+1}/{len(plan)}"
                })
            
            # Create and execute sub-agent
            # CRITICAL: Inject the original user_input (Global Goal) into context
            # so the SubAgent knows WHAT content to generate (e.g. "PDF about AI Agents")
            # and doesn't just produce generic output.
            full_context = f"GLOBAL GOAL: {user_input}\n\nSTEP CONTEXT: {step.context}\n\nPrevious results:\n" + "\n".join(results[-2:])
            
            task_def = TaskDefinition(
                id=step.id,
                objective=step.objective,
                context=full_context
            )
            
            sub_agent = SubAgent(task_def, self.tools, self.client, self.model, self.pipeline)
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
                
                # Log successful step to pipeline
                if self.pipeline:
                    for file_path in task_result.files_created:
                        self.pipeline.add_event("file_created", path=file_path, step_id=step.id)
                    for file_path in task_result.files_modified:
                        self.pipeline.add_event("file_modified", path=file_path, step_id=step.id)
                    self.pipeline.add_event(
                        "validation",
                        step_id=step.id,
                        success=True,
                        confidence=validation.confidence,
                        feedback=validation.feedback
                    )
                
                if callback:
                    await callback({
                        "type": "step_completed",
                        "step_id": step.id,
                        "validation": {"success": True, "feedback": validation.feedback}
                    })
            else:
                step.status = "failed"
                results.append(f"✗ {step.objective}: {validation.feedback}")
                
                # Log failed step to pipeline
                if self.pipeline:
                    self.pipeline.add_event(
                        "validation",
                        step_id=step.id,
                        success=False,
                        confidence=validation.confidence,
                        feedback=validation.feedback
                    )
                
                if callback:
                    await callback({
                        "type": "step_failed",
                        "step_id": step.id,
                        "validation": {"success": False, "feedback": validation.feedback}
                    })
                
                # For now, continue despite failure (future: retry logic)
            
            # Save updated status after step
            self._save_plan_state()
        
        # Clear plan state on completion
        self._clear_plan_state()
        
        # Step 3: Generate final summary
        summary = "Task completed. Results:\n" + "\n".join(results)
        return summary

    def _save_plan_state(self):
        """Save the current plan state to file for resumption."""
        if not self.project_id or not self.current_plan:
            return
            
        if not self.sandbox:
            return

        # Save to project workspace
        plan_path = os.path.join(self.sandbox.workspace_path, ".active_plan.json")
        
        try:
            state = {
                "plan": [
                    {
                        "id": s.id, 
                        "objective": s.objective, 
                        "context": s.context, 
                        "status": s.status
                    } for s in self.current_plan
                ],
                "last_status": "in_progress"
            }
            with open(plan_path, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Failed to save plan state: {e}")

    def _clear_plan_state(self):
        """Delete specific plan state file after completion."""
        if not self.project_id:
            return
        if not self.sandbox:
            return
        plan_path = os.path.join(self.sandbox.workspace_path, ".active_plan.json")
        if os.path.exists(plan_path):
            try:
                os.remove(plan_path)
            except:
                pass

    async def _generate_plan(self, user_input: str) -> List[PlanStep]:
        """Generate a structured execution plan."""
        
        response = await self.client.chat.completions.create(
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
