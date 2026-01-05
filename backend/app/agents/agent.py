"""
OrchestratorAgent - Main agent that processes user requests and uses tools.
"""

import os
import json
import traceback
from openai import OpenAI
from dotenv import load_dotenv
from typing import Callable, Optional
from app.agents.sandbox import Sandbox, sandbox_manager
from app.tools.registry import ToolRegistry, ToolResult
from app.agents.chat_history import chat_history_manager

load_dotenv()


class OrchestratorAgent:
    """
    Main agent that orchestrates task execution.
    Uses tools to interact with the sandbox environment.
    """

    SYSTEM_PROMPT = """You are a versatile AI assistant with access to a sandboxed workspace.

You have tools to interact with files and execute commands. Use them to accomplish whatever the user asks.

CORE PRINCIPLES:
1. **Understand the request** - What does the user actually want?
2. **Plan dynamically** - Figure out the best approach using available tools
3. **Execute proactively** - Don't just explain, DO the work
4. **Adapt and iterate** - If something fails, debug and fix it
5. **Be thorough** - Complete the task fully

You are not limited to any specific domain. Use your tools creatively to solve any problem."""

    def __init__(self, project_id: Optional[str] = None):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

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

        if project_id:
            self.set_project(project_id)

        # Conversation history
        self.messages = []

    def set_project(self, project_id: str):
        """Set the current project and initialize its sandbox."""
        self.project_id = project_id
        self.sandbox = sandbox_manager.get_or_create(project_id)
        self.tools = ToolRegistry(self.sandbox)
        # Load chat history for this project
        self.messages = chat_history_manager.load(project_id)

    def get_tools_schema(self) -> list[dict]:
        """Get the tools schema for the API call."""
        if not self.tools:
            return []
        return self.tools.list_tools()

    async def run(
        self,
        user_input: str,
        callback: Optional[Callable] = None
    ) -> str:
        """
        Process user input and execute any necessary tool calls.

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

        # Notify start
        if callback:
            await callback({
                "type": "status",
                "status": "thinking",
                "message": "Processing your request..."
            })

        try:
            # Initial API call with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    *self.messages
                ],
                tools=self.get_tools_schema(),
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Process tool calls in a loop until no more tools are called
            max_iterations = 10  # Safety limit
            iteration = 0

            while assistant_message.tool_calls and iteration < max_iterations:
                iteration += 1

                # Add assistant's message with tool calls to history
                self.messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        arguments = {}

                    # Notify tool execution
                    if callback:
                        await callback({
                            "type": "tool_call",
                            "tool": tool_name,
                            "arguments": arguments,
                            "status": "executing"
                        })

                    # Execute the tool
                    result = await self.tools.execute(tool_name, arguments)

                    # Notify tool result
                    if callback:
                        await callback({
                            "type": "tool_result",
                            "tool": tool_name,
                            "success": result.success,
                            "output": result.output[:500] if len(result.output) > 500 else result.output,
                            "data": result.data
                        })

                    # Add tool result to messages
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.output
                    })

                # Get next response from the model
                if callback:
                    await callback({
                        "type": "status",
                        "status": "thinking",
                        "message": "Analyzing results..."
                    })

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        *self.messages
                    ],
                    tools=self.get_tools_schema(),
                    tool_choice="auto"
                )

                assistant_message = response.choices[0].message

            # Final response (no more tool calls)
            final_content = assistant_message.content or "Task completed."

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
            traceback.print_exc()
            return error_msg

    def clear_history(self):
        """Clear conversation history."""
        self.messages = []

    def get_workspace_info(self) -> dict:
        """Get information about the current workspace."""
        if not self.sandbox:
            return {"error": "No project selected"}
        return self.sandbox.get_workspace_info()
