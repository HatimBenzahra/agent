"""
SubAgent module - Executes individual tasks in isolation.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from openai import AsyncOpenAI


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
        llm_client: AsyncOpenAI,
        model: str,
        pipeline=None  # Optional SessionPipeline for event logging
    ):
        self.task = task
        self.tools = tools_registry
        self.client = llm_client
        self.model = model
        self.pipeline = pipeline
        
        # Track execution
        self.tools_used = []
        self.files_created = []
        self.files_modified = []
        self.terminal_outputs = []
    
    async def execute(self, callback: Optional[Callable] = None) -> TaskResult:
        """Execute the task using tools."""
        
        # Loop settings
        max_iterations = 15
        
        system_prompt = f"""You are an autonomous AI problem solver.
        
YOUR TASK:
{self.task.objective}

CONTEXT:
{self.task.context}

CORE BEHAVIOR:
1. **ANALYZE**: Understand what needs to be done. If you don't know how, SEARCH or EXPLORE first.
2. **ACT**: Use your tools (terminal, write_file, etc.) to make progress.
3. **OBSERVE**: Watch the output of your commands. Did it work? Did it fail?
4. **ITERATE**: 
   - If success -> Great, move to next step.
   - If failure -> READ THE ERROR. Analyze it. Propose a fix. Try again.
   - **DO NOT GIVE UP**. You are expected to solve problems, not just report them.

TOOLS AVAILABLE:
- `write_file`: Create/edit files. (Use this for code, configs, notes).
- `terminal`: Run ANY shell command. (python, pip, ls, grep, curl, etc.).
- `read_file`: Read content of files.
- `list_files`: See directory structure.
- `search`: Search the web (if available) or codebase.

CRITICAL RULES:
- **NO HARDCODED WORKFLOWS**: You decide the best path. You can run python code, shell scripts, or just check files.
- **SELF-CORRECTION**: If a command fails (e.g. 'command not found'), try an alternative. If a library is missing, install it.
- **BE RESOURCEFUL**: If you need to manipulate a PDF and don't know how, write a script to check available libraries first.
- **FINAL OUTPUT**: Your goal is to achieve the OBJECTIVE. The output should be the result of that achievement.

EXAMPLE - User wants to "check disk space":
- You: terminal('df -h') -> Done.

EXAMPLE - User wants to "convert CSV to JSON":
- You: 
  1. Check if input file exists (ls).
  2. Write a customized python script to convert it.
  3. Run the script.
  4. If script fails with "pandas not found", you runs "pip install pandas" and tries again.

You have {max_iterations} turns to solve this. Make them count.
Start NOW."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Execute: {self.task.objective}"}
        ]
        
        try:
            # Loop until no more tool calls
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                response = await self.client.chat.completions.create(
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
            # Log to pipeline
            if self.pipeline:
                self.pipeline.add_event(
                    "terminal_command",
                    command=args.get('command', ''),
                    output=result.output[:500],  # Truncate
                    success=result.success
                )
        
        # Notify via callback
        if callback:
            await callback({
                "type": "sub_agent_tool",
                "task_id": self.task.id,
                "tool": tool_name,
                "arguments": args,
                "success": result.success,
                "output": result.output[:500] if result.output else ""
            })
        
        return result.output or ("Success" if result.success else f"Error: {result.output}")
