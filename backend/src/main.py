import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from api.db import init_db
from api.chat import models
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #before app startup
    init_db()
    yield
    #after startup

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats")

# Serve the chat frontend at the root URL
FRONTEND_DIR = Path(__file__).parent / "frontend"

@app.get("/", response_class=HTMLResponse)
def chat_page():
    html_file = FRONTEND_DIR / "index.html"
    return HTMLResponse(content=html_file.read_text(), status_code=200)

@app.get("/ai-mail-icon.png")
def get_favicon():
    icon_path = FRONTEND_DIR / "ai-mail-icon.png"
    if icon_path.exists():
        return FileResponse(icon_path)
    return HTMLResponse(status_code=404)