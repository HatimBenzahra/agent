"""
FastAPI server with WebSocket support for the agent.
Handles projects, chat, and terminal streaming.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from typing import Optional
import traceback
import json
import os
import mimetypes

try:
    from .agent import OrchestratorAgent
    from .projects import project_manager
    from .sandbox import sandbox_manager
except ImportError:
    from app.agents.agent import OrchestratorAgent
    from app.agents.projects import project_manager
    from app.agents.sandbox import sandbox_manager

router = APIRouter()

# Store active agents per project
agents: dict[str, OrchestratorAgent] = {}


def get_agent(project_id: str) -> OrchestratorAgent:
    """Get or create an agent for a project."""
    if project_id not in agents:
        agents[project_id] = OrchestratorAgent(project_id)
    return agents[project_id]


# ============== Project Endpoints ==============

class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = ""


class UpdateProjectRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


@router.get("/api/projects")
async def list_projects():
    """List all projects."""
    projects = project_manager.list_all()
    return {"projects": [p.to_dict() for p in projects]}


@router.post("/api/projects")
async def create_project(request: CreateProjectRequest):
    """Create a new project."""
    project = project_manager.create(request.name, request.description)
    # Initialize sandbox for the project
    sandbox_manager.get_or_create(project.id)
    return {"project": project.to_dict()}


@router.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get a specific project."""
    project = project_manager.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": project.to_dict()}


@router.patch("/api/projects/{project_id}")
async def update_project(project_id: str, request: UpdateProjectRequest):
    """Update a project."""
    project = project_manager.update(
        project_id,
        name=request.name,
        description=request.description
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": project.to_dict()}


@router.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and its workspace."""
    success = project_manager.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

    # Clean up sandbox
    sandbox_manager.delete(project_id)

    # Remove agent if exists
    if project_id in agents:
        del agents[project_id]

    return {"success": True}


# ============== Workspace Endpoints ==============

@router.get("/api/projects/{project_id}/files")
async def list_files(project_id: str, path: str = "."):
    """List files in project workspace."""
    sandbox = sandbox_manager.get_or_create(project_id)
    files = sandbox.list_files(path)
    return {"files": [f.__dict__ for f in files]}


@router.get("/api/projects/{project_id}/files/content")
async def read_file(project_id: str, path: str, raw: bool = False):
    """Read file content. Use raw=true for binary files like PDFs."""
    sandbox = sandbox_manager.get_or_create(project_id)

    # For raw/binary files (PDF, images, etc.)
    if raw:
        file_path = sandbox.workspace_path / path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Security check - ensure path is within workspace
        try:
            file_path.resolve().relative_to(sandbox.workspace_path.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="Access denied")

        # Detect mime type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        return FileResponse(
            path=str(file_path),
            media_type=mime_type,
            filename=os.path.basename(path)
        )

    # For text files (default behavior)
    success, content = sandbox.read_file(path)
    if not success:
        raise HTTPException(status_code=404, detail=content)
    return {"content": content, "path": path}


class WriteFileRequest(BaseModel):
    path: str
    content: str


@router.post("/api/projects/{project_id}/files")
async def write_file(project_id: str, request: WriteFileRequest):
    """Write file content."""
    sandbox = sandbox_manager.get_or_create(project_id)
    success, message = sandbox.write_file(request.path, request.content)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.delete("/api/projects/{project_id}/files")
async def delete_file(project_id: str, path: str):
    """Delete a file."""
    sandbox = sandbox_manager.get_or_create(project_id)
    success, message = sandbox.delete_file(path)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.get("/api/projects/{project_id}/chat/history")
async def get_chat_history(project_id: str):
    """Get chat history for a project."""
    from app.agents.chat_history import chat_history_manager
    messages = chat_history_manager.load(project_id)
    return {"messages": messages}


# ============== WebSocket Endpoints ==============

@router.websocket("/ws/chat/{project_id}")
async def websocket_chat(websocket: WebSocket, project_id: str):
    """
    WebSocket endpoint for chat with the agent.
    Streams tool calls and results in real-time.
    Includes ping-pong heartbeat to keep connection alive.
    """
    await websocket.accept()
    print(f"Client connected to project: {project_id}")

    # Ensure project exists
    project = project_manager.get(project_id)
    if not project:
        await websocket.send_json({"type": "error", "content": "Project not found"})
        await websocket.close()
        return

    # Get or create agent for this project
    agent = get_agent(project_id)

    try:
        while True:
            data = await websocket.receive_text()

            # Handle ping-pong heartbeat to keep connection alive
            if data == "ping":
                await websocket.send_text("pong")
                continue

            print(f"[{project_id}] Received: {data}")

            # Define callback to stream events to client
            async def progress_callback(event):
                try:
                    await websocket.send_json(event)
                except RuntimeError:
                    # Connection closed
                    pass
                except Exception as e:
                    print(f"Error sending callback event: {e}")

            try:
                # Run agent with callback
                response = await agent.run(data, callback=progress_callback)

                # Send final answer
                try:
                    await websocket.send_json({
                        "type": "result",
                        "content": response
                    })

                    # Send updated file list
                    files = agent.sandbox.list_files() if agent.sandbox else []
                    await websocket.send_json({
                        "type": "files_updated",
                        "files": [f.__dict__ for f in files]
                    })
                except RuntimeError:
                    pass

            except Exception as e:
                print(f"Error executing agent: {e}")
                traceback.print_exc()
                try:
                    await websocket.send_json({
                        "type": "error",
                        "content": str(e)
                    })
                except RuntimeError:
                    pass

    except WebSocketDisconnect:
        print(f"Client disconnected from project: {project_id}")


@router.websocket("/ws/terminal/{project_id}")
async def websocket_terminal(websocket: WebSocket, project_id: str):
    """
    WebSocket endpoint for direct terminal access.
    Allows the user to run commands in the project sandbox.
    """
    await websocket.accept()
    print(f"Terminal connected to project: {project_id}")

    sandbox = sandbox_manager.get_or_create(project_id)

    try:
        # Send initial prompt
        await websocket.send_json({
            "type": "prompt",
            "cwd": "/"
        })

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "command":
                command = message.get("command", "")
                print(f"[{project_id}] Terminal: {command}")

                # Execute command
                result = await sandbox.execute(command)

                # Send result
                await websocket.send_json({
                    "type": "output",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.return_code,
                    "duration": result.duration
                })

                # Send new prompt with updated cwd
                cwd = str(sandbox.current_dir.relative_to(sandbox.workspace_path))
                await websocket.send_json({
                    "type": "prompt",
                    "cwd": f"/{cwd}" if cwd != "." else "/"
                })

    except WebSocketDisconnect:
        print(f"Terminal disconnected from project: {project_id}")


# ============== Health Check ==============


