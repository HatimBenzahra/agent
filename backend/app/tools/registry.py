"""
Tools module - Defines tools that the agent can use.
Each tool is a function that the agent can call to interact with the sandbox.
"""

from typing import Callable, Any
from dataclasses import dataclass

from app.agents.sandbox import Sandbox


@dataclass
class ToolResult:
    """Result of a tool execution."""
    success: bool
    output: str
    data: Any = None


@dataclass
class Tool:
    """Definition of a tool available to the agent."""
    name: str
    description: str
    parameters: dict  # JSON Schema for parameters
    execute: Callable  # Function to execute


class ToolRegistry:
    """Registry of available tools for the agent."""

    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox
        self.tools: dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register the default set of tools."""

        # Terminal tool - execute shell commands
        self.register(Tool(
            name="terminal",
            description="Execute a shell command in the project workspace. Use this to run code, install packages, or perform any terminal operation.",
            parameters={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                    }
                },
                "required": ["command"]
            },
            execute=self._execute_terminal
        ))

        # Write file tool
        self.register(Tool(
            name="write_file",
            description="Create or overwrite a file in the project workspace. Use this to write code, configuration files, or any text content.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to the workspace root (e.g., 'src/main.py', 'index.html')"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                },
                "required": ["path", "content"]
            },
            execute=self._execute_write_file
        ))

        # Read file tool
        self.register(Tool(
            name="read_file",
            description="Read the contents of a file in the project workspace.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path relative to the workspace root"
                    }
                },
                "required": ["path"]
            },
            execute=self._execute_read_file
        ))

        # List files tool
        self.register(Tool(
            name="list_files",
            description="List files and directories in the project workspace.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path relative to the workspace root. Defaults to root.",
                        "default": "."
                    }
                },
                "required": []
            },
            execute=self._execute_list_files
        ))

        # Delete file tool
        self.register(Tool(
            name="delete_file",
            description="Delete a file or directory in the project workspace.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File or directory path to delete"
                    }
                },
                "required": ["path"]
            },
            execute=self._execute_delete_file
        ))

    def register(self, tool: Tool):
        """Register a new tool."""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Get a tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> list[dict]:
        """List all available tools in OpenAI function format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        """Execute a tool by name with given arguments."""
        tool = self.tools.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                output=f"Unknown tool: {tool_name}"
            )

        try:
            return await tool.execute(arguments)
        except Exception as e:
            return ToolResult(
                success=False,
                output=f"Tool execution error: {str(e)}"
            )

    # Tool implementations

    async def _execute_terminal(self, args: dict) -> ToolResult:
        """Execute a terminal command."""
        command = args.get("command", "")
        if not command:
            return ToolResult(success=False, output="No command provided")

        result = await self.sandbox.execute(command)

        output_parts = []
        if result.stdout:
            output_parts.append(result.stdout)
        if result.stderr:
            output_parts.append(f"[stderr] {result.stderr}")

        output = "\n".join(output_parts) if output_parts else "(no output)"

        return ToolResult(
            success=result.return_code == 0,
            output=output,
            data={
                "command": command,
                "return_code": result.return_code,
                "duration": result.duration
            }
        )

    async def _execute_write_file(self, args: dict) -> ToolResult:
        """Write content to a file."""
        path = args.get("path", "")
        content = args.get("content", "")

        if not path:
            return ToolResult(success=False, output="No file path provided")

        success, message = self.sandbox.write_file(path, content)

        return ToolResult(
            success=success,
            output=message,
            data={"path": path, "size": len(content)}
        )

    async def _execute_read_file(self, args: dict) -> ToolResult:
        """Read content from a file."""
        path = args.get("path", "")

        if not path:
            return ToolResult(success=False, output="No file path provided")

        success, content = self.sandbox.read_file(path)

        return ToolResult(
            success=success,
            output=content,
            data={"path": path}
        )

    async def _execute_list_files(self, args: dict) -> ToolResult:
        """List files in a directory."""
        path = args.get("path", ".")

        files = self.sandbox.list_files(path)

        if not files:
            return ToolResult(
                success=True,
                output="(empty directory)",
                data={"files": []}
            )

        # Format output
        lines = []
        for f in files:
            icon = "/" if f.is_dir else ""
            size = f"{f.size}B" if not f.is_dir else ""
            lines.append(f"{f.name}{icon} {size}".strip())

        return ToolResult(
            success=True,
            output="\n".join(lines),
            data={"files": [f.__dict__ for f in files]}
        )

    async def _execute_delete_file(self, args: dict) -> ToolResult:
        """Delete a file or directory."""
        path = args.get("path", "")

        if not path:
            return ToolResult(success=False, output="No path provided")

        success, message = self.sandbox.delete_file(path)

        return ToolResult(
            success=success,
            output=message,
            data={"path": path}
        )
