from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints

app = FastAPI(title="Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the endpoints router
# The previous server.py had paths like /api/projects and /ws/chat
# so we include it at root.
app.include_router(endpoints.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
