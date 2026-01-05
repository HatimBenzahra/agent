"""
SubAgent module - Executes individual tasks in isolation.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from openai import OpenAI


@dataclass
class TaskDefinition:
    """Definition of a task to be executed."""
    id: str
    objective: str
    context: str  # Additional context from previous steps
    required_tools: List[str] = field(default_factory=list)


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    success: bool
    output: str
    tools_used: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    terminal_output: str = ""
    error: Optional[str] = None


class SubAgent:
    """
    Executes a single task in isolation.
    Focused on one specific objective with limited scope.
    """
    
    def __init__(
        self,
        task: TaskDefinition,
        tools_registry,
        llm_client: OpenAI,
        model: str
    ):
        self.task = task
        self.tools = tools_registry
        self.client = llm_client
        self.model = model
        
        # Track execution
        self.tools_used = []
        self.files_created = []
        self.files_modified = []
        self.terminal_outputs = []
    
    async def execute(self, callback: Optional[Callable] = None) -> TaskResult:
        """Execute the task using tools."""
        
        system_prompt = f"""You are a specialized task executor.

YOUR TASK:
{self.task.objective}

CONTEXT:
{self.task.context}

CRITICAL RULES:
1. You MUST use the provided tools to complete the task.
2. If you need to create a file, you MUST use the `write_file` tool.
3. DO NOT just output the code in your response. The user CANNOT see your response code, only the files you create.
4. If you write code, you MUST run it using the `terminal` tool to verify it works.
5. Create files first, then execute them.

EXAMPLE:
- User: "Create a python script"
- Bad Response: "Here is the code: print('hello')"
- Good Response: calls write_file('script.py', "print('hello')") then calls terminal('python script.py')

Start by using a tool immediately.

CHECKLIST BEFORE ANSWERING:
- Did I write the file? (Use write_file)
- Did I run the code? (Use terminal)
- Did I see the output?
- If I am just talking, I AM FAILING. I MUST ACT."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Execute: {self.task.objective}"}
        ]
        
        try:
            # Loop until no more tool calls
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools.list_tools(),
                    tool_choice="auto"
                )
                
                message = response.choices[0].message
                
                if not message.tool_calls:
                    # No more tool calls, we're done
                    return TaskResult(
                        task_id=self.task.id,
                        success=True,
                        output=message.content or "",
                        tools_used=self.tools_used,
                        files_created=self.files_created,
                        files_modified=self.files_modified,
                        terminal_output="\n".join(self.terminal_outputs)
                    )
                
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })
                
                # Execute each tool call and add results
                for tool_call in message.tool_calls:
                    tool_result = await self._execute_tool(tool_call, callback)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
            
            # Max iterations reached
            return TaskResult(
                task_id=self.task.id,
                success=True,
                output="Task completed (max iterations reached)",
                tools_used=self.tools_used,
                files_created=self.files_created,
                files_modified=self.files_modified,
                terminal_output="\n".join(self.terminal_outputs)
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return TaskResult(
                task_id=self.task.id,
                success=False,
                output="",
                tools_used=self.tools_used,
                files_created=self.files_created,
                files_modified=self.files_modified,
                terminal_output="\n".join(self.terminal_outputs),
                error=str(e)
            )
    
    async def _execute_tool(self, tool_call, callback) -> str:
        """Execute a single tool call and return result."""
        tool_name = tool_call.function.name
        
        try:
            args = json.loads(tool_call.function.arguments)
        except:
            args = {}
        
        # Track tool usage
        self.tools_used.append(tool_name)
        
        # Execute
        result = await self.tools.execute(tool_name, args)
        
        # Track file operations
        if tool_name == "write_file" and result.success:
            path = args.get("path", "")
            if path not in self.files_created:
                self.files_created.append(path)
        
        if tool_name == "terminal" and result.output:
            self.terminal_outputs.append(result.output)
        
        # Notify via callback
        if callback:
            await callback({
                "type": "sub_agent_tool",
                "task_id": self.task.id,
                "tool": tool_name,
                "success": result.success,
                "output": result.output[:200] if result.output else ""
            })
        
        return result.output or ("Success" if result.success else f"Error: {result.output}")
