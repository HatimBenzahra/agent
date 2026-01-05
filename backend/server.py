from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .agent import OrchestratorAgent
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = OrchestratorAgent()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            
            # Define callback to stream logs to client
            async def progress_callback(event):
                await websocket.send_json(event)

            try:
                # Run agent with callback
                response = await agent.run(data, callback=progress_callback)
                
                # Send final answer
                await websocket.send_json({
                    "type": "result", 
                    "content": response
                })
            except Exception as e:
                print(f"Error executing agent: {e}")
                traceback.print_exc()
                await websocket.send_json({
                    "type": "error", 
                    "content": str(e)
                })

    except WebSocketDisconnect:
        print("Client disconnected")
