# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_health import router as health_router
from app.api.routes_upload import router as upload_router

# Correct imports
from app.api.routes_chat import router as chat_router       # /ask
from app.api.routes_chats import router as chats_router     # /chats

app = FastAPI(title="Klarity Backend - Minimal API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)     # /ask
app.include_router(chats_router)    # /chats
