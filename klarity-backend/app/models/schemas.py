# app/models/schemas.py

from pydantic import BaseModel
from datetime import datetime


# ==========================
# Chat Schemas
# ==========================

class ChatCreate(BaseModel):
    title: str


class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # allows returning SQLAlchemy objects directly


# ==========================
# Message Schemas
# ==========================

class MessageOut(BaseModel):
    id: int
    chat_id: int
    role: str           # "user" or "assistant"
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True


# ==========================
# Document Schemas
# ==========================

class DocumentOut(BaseModel):
    id: int
    chat_id: int
    file_name: str
    doc_id: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


# ==========================
# Ask / QA Schemas
# ==========================

class AskRequest(BaseModel):
    question: str
