from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

app = FastAPI(title="Orchestrator Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Chat Router
# The websocket will be at /ws/chat because we prefix it here
app.include_router(chat.router, prefix="/ws")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Orchestrator Agent is running"}
