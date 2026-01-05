from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.agent import OrchestratorAgent
import traceback

router = APIRouter()
agent = OrchestratorAgent()

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected via Reorganized Architecture")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            
            async def progress_callback(event):
                await websocket.send_json(event)

            try:
                response = await agent.run(data, callback=progress_callback)
                await websocket.send_json({"type": "result", "content": response})
            except Exception as e:
                print(f"Error executing agent: {e}")
                traceback.print_exc()
                await websocket.send_json({"type": "error", "content": str(e)})

    except WebSocketDisconnect:
        print("Client disconnected")
