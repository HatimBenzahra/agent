"""
Sandbox module - Manages isolated workspaces for agent execution.
Each project gets its own directory where the agent can create files and run commands.
"""

import os
import subprocess
import asyncio
import shutil
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

# Base directory for all project workspaces
WORKSPACES_DIR = Path(__file__).parent.parent / "workspaces"


@dataclass
class CommandResult:
    """Result of a command execution."""
    command: str
    stdout: str
    stderr: str
    return_code: int
    duration: float


@dataclass
class FileInfo:
    """Information about a file in the workspace."""
    name: str
    path: str
    is_dir: bool
    size: int
    modified: str


class Sandbox:
    """
    Sandbox environment for a single project.
    Provides isolated file system and command execution.
    """

    # Whitelist of allowed commands (base commands, can be extended)
    ALLOWED_COMMANDS = {
        'python', 'python3', 'pip', 'pip3',
        'node', 'npm', 'npx',
        'ls', 'cat', 'head', 'tail', 'grep', 'find',
        'mkdir', 'touch', 'cp', 'mv', 'rm',
        'echo', 'pwd', 'which', 'env',
        'git', 'curl', 'wget',
        'cd',
        'g++', 'gcc', 'make', 'cmake', 'cc', 'c++', 'clang', 'clang++',  # Handled specially
    }

    # Dangerous patterns to block
    BLOCKED_PATTERNS = [
        'sudo', 'su ', 'chmod 777', 'rm -rf /',
        '/etc/', '/usr/', '/bin/', '/sbin/',
        '~/', '../', '$HOME',
        'eval', 'exec',
    ]

    def __init__(self, project_id: str, workspace_path: Path):
        self.project_id = project_id
        self.workspace_path = workspace_path
        self.current_dir = workspace_path
        self._ensure_workspace()

    def _ensure_workspace(self):
        """Create workspace directory if it doesn't exist."""
        self.workspace_path.mkdir(parents=True, exist_ok=True)

    def _is_command_allowed(self, command: str) -> tuple[bool, str]:
        """
        Check if a command is allowed to run.
        Returns (allowed, reason).
        """
        # Check for blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in command:
                return False, f"Blocked pattern detected: {pattern}"

        # Extract base command
        parts = command.strip().split()
        if not parts:
            return False, "Empty command"

        base_cmd = parts[0]

        # Allow commands in whitelist
        if base_cmd in self.ALLOWED_COMMANDS:
            return True, "OK"

        # Allow running scripts in workspace
        if base_cmd.startswith('./') or base_cmd.startswith('python'):
            return True, "OK"

        return False, f"Command not in whitelist: {base_cmd}"

    def _resolve_path(self, path: str) -> Path:
        """
        Resolve a path relative to current directory.
        Ensures path stays within workspace.
        """
        if path.startswith('/'):
            # Absolute path - make it relative to workspace
            resolved = self.workspace_path / path.lstrip('/')
        else:
            resolved = self.current_dir / path

        # Resolve and check it's within workspace
        resolved = resolved.resolve()

        try:
            resolved.relative_to(self.workspace_path)
            return resolved
        except ValueError:
            # Path escapes workspace, return workspace root
            return self.workspace_path

    async def execute(self, command: str, timeout: int = 30) -> CommandResult:
        """
        Execute a command in the sandbox.

        Args:
            command: Shell command to execute
            timeout: Maximum execution time in seconds

        Returns:
            CommandResult with stdout, stderr, return code
        """
        start_time = asyncio.get_event_loop().time()

        # Check if command is allowed
        allowed, reason = self._is_command_allowed(command)
        if not allowed:
            return CommandResult(
                command=command,
                stdout="",
                stderr=f"Command blocked: {reason}",
                return_code=1,
                duration=0
            )

        # Handle cd specially
        if command.strip().startswith('cd '):
            target = command.strip()[3:].strip()
            new_dir = self._resolve_path(target)
            if new_dir.is_dir():
                self.current_dir = new_dir
                rel_path = new_dir.relative_to(self.workspace_path)
                return CommandResult(
                    command=command,
                    stdout=f"Changed directory to /{rel_path}" if str(rel_path) != '.' else "Changed to workspace root",
                    stderr="",
                    return_code=0,
                    duration=0
                )
            else:
                return CommandResult(
                    command=command,
                    stdout="",
                    stderr=f"Directory not found: {target}",
                    return_code=1,
                    duration=0
                )

        try:
            # Run command in subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.current_dir),
                env={
                    **os.environ,
                    'HOME': str(self.workspace_path),
                    'PWD': str(self.current_dir),
                }
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return CommandResult(
                    command=command,
                    stdout="",
                    stderr=f"Command timed out after {timeout}s",
                    return_code=-1,
                    duration=timeout
                )

            duration = asyncio.get_event_loop().time() - start_time

            return CommandResult(
                command=command,
                stdout=stdout.decode('utf-8', errors='replace'),
                stderr=stderr.decode('utf-8', errors='replace'),
                return_code=process.returncode or 0,
                duration=duration
            )

        except Exception as e:
            return CommandResult(
                command=command,
                stdout="",
                stderr=str(e),
                return_code=1,
                duration=0
            )

    def write_file(self, path: str, content: str) -> tuple[bool, str]:
        """
        Write content to a file in the workspace.

        Args:
            path: File path relative to workspace
            content: File content

        Returns:
            (success, message)
        """
        try:
            file_path = self._resolve_path(path)

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_text(content, encoding='utf-8')

            rel_path = file_path.relative_to(self.workspace_path)
            return True, f"File written: /{rel_path}"

        except Exception as e:
            return False, str(e)

    def read_file(self, path: str) -> tuple[bool, str]:
        """
        Read content from a file in the workspace.

        Args:
            path: File path relative to workspace

        Returns:
            (success, content_or_error)
        """
        try:
            file_path = self._resolve_path(path)

            if not file_path.exists():
                return False, f"File not found: {path}"

            if not file_path.is_file():
                return False, f"Not a file: {path}"

            content = file_path.read_text(encoding='utf-8')
            return True, content

        except Exception as e:
            return False, str(e)

    def list_files(self, path: str = ".") -> list[FileInfo]:
        """
        List files in a directory.

        Args:
            path: Directory path relative to workspace

        Returns:
            List of FileInfo objects
        """
        try:
            dir_path = self._resolve_path(path)

            if not dir_path.is_dir():
                return []

            files = []
            for item in sorted(dir_path.iterdir()):
                stat = item.stat()
                rel_path = item.relative_to(self.workspace_path)
                files.append(FileInfo(
                    name=item.name,
                    path=f"/{rel_path}",
                    is_dir=item.is_dir(),
                    size=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime).isoformat()
                ))

            return files

        except Exception:
            return []

    def delete_file(self, path: str) -> tuple[bool, str]:
        """Delete a file or directory."""
        try:
            file_path = self._resolve_path(path)

            if not file_path.exists():
                return False, f"Path not found: {path}"

            # Don't allow deleting workspace root
            if file_path == self.workspace_path:
                return False, "Cannot delete workspace root"

            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()

            return True, f"Deleted: {path}"

        except Exception as e:
            return False, str(e)

    def get_workspace_info(self) -> dict:
        """Get information about the workspace."""
        return {
            "project_id": self.project_id,
            "workspace_path": str(self.workspace_path),
            "current_dir": str(self.current_dir.relative_to(self.workspace_path)),
            "files": [f.__dict__ for f in self.list_files()]
        }

    def cleanup(self):
        """Remove the entire workspace."""
        if self.workspace_path.exists():
            shutil.rmtree(self.workspace_path)


class SandboxManager:
    """Manages multiple sandbox instances for different projects."""

    def __init__(self):
        self.sandboxes: dict[str, Sandbox] = {}
        WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)

    def get_or_create(self, project_id: str) -> Sandbox:
        """Get existing sandbox or create new one for a project."""
        if project_id not in self.sandboxes:
            workspace_path = WORKSPACES_DIR / project_id
            self.sandboxes[project_id] = Sandbox(project_id, workspace_path)

        return self.sandboxes[project_id]

    def delete(self, project_id: str):
        """Delete a sandbox and its workspace."""
        if project_id in self.sandboxes:
            self.sandboxes[project_id].cleanup()
            del self.sandboxes[project_id]

    def list_all(self) -> list[str]:
        """List all project IDs with workspaces."""
        if not WORKSPACES_DIR.exists():
            return []
        return [d.name for d in WORKSPACES_DIR.iterdir() if d.is_dir()]


# Global sandbox manager instance
sandbox_manager = SandboxManager()
