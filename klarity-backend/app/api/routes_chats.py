# app/api/routes_chats.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os

from app.db.database import get_db
from app.db.models import Chat, Document, Message
from app.models.schemas import ChatCreate, ChatOut, AskRequest
from app.utils.file_utils import save_upload_file
from app.services.extractor_adapter import run_extraction
from app.db.qdrant_client import upsert_embeddings

# Use your adapters (document-based pipeline)
from app.services.cleaner_adapter import clean_documents
from app.services.chunking_adapter import chunk_documents
from app.services.embedder_adapter import embed_documents

from app.qa import answer_question_for_chat

router = APIRouter(tags=["chats"])


# ================================
# 1️⃣ Create Chat
# ================================
@router.post("/chats", response_model=ChatOut)
def create_chat(payload: ChatCreate, db: Session = Depends(get_db)):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Chat title cannot be empty.")

    chat = Chat(title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


# ================================
# 2️⃣ List Chats
# ================================
@router.get("/chats", response_model=List[ChatOut])
def list_chats(db: Session = Depends(get_db)):
    chats = db.query(Chat).order_by(Chat.created_at.desc()).all()
    return chats


# ================================
# 3️⃣ Upload PDF to a specific chat
# ================================
@router.post("/chats/{chat_id}/upload")
async def upload_file_to_chat(
    chat_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 0) Check chat exists
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    # 1) Save the file
    saved_path = save_upload_file(file)
    if not os.path.exists(saved_path):
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    # 2) Extract documents (list[Document]) from file
    try:
        extracted_docs = run_extraction(saved_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {e}")

    if not extracted_docs:
        raise HTTPException(status_code=500, detail="Extractor returned no documents.")

    # 3) Clean docs (same Cleaner pipeline you already use)
    try:
        cleaned_docs = clean_documents(extracted_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning error: {e}")

    if not cleaned_docs:
        raise HTTPException(status_code=500, detail="Cleaning produced no documents.")

    # 4) Chunk docs
    try:
        chunked_docs = chunk_documents(cleaned_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chunking error: {e}")

    if not chunked_docs:
        raise HTTPException(status_code=500, detail="No chunks generated from documents.")

    # 5) Embed chunks via Embedder adapter
    try:
        embedded_items = embed_documents(chunked_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    if not embedded_items:
        raise HTTPException(status_code=500, detail="No embeddings generated.")

    # Split into vectors + payloads for Qdrant
    vectors: List[List[float]] = []
    payloads: List[dict] = []

    doc_id = os.path.basename(saved_path)  # used both in DB and Qdrant payload
    collection_name = f"klarity_chat_{chat_id}"

    for item in embedded_items:
        vec = item.get("embedding")
        text = item.get("text", "")
        meta = item.get("metadata", {}) or {}

        if not vec:
            continue

        vectors.append(vec)
        payloads.append(
            {
                "chat_id": chat_id,
                "doc_id": doc_id,
                "text": text,
                **meta,  # keep page/chunk_index etc.
            }
        )

    if not vectors:
        raise HTTPException(status_code=500, detail="No valid vectors to upsert.")

    # 6) Upsert into Qdrant, per-chat collection
    try:
        upsert_embeddings(collection_name, vectors, payloads)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qdrant upsert error: {e}")

    # 7) Save document record in DB
    doc = Document(
        chat_id=chat_id,
        file_name=os.path.basename(saved_path),
        doc_id=doc_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # some simple stats for debug
    raw_length = sum(len(d.page_content or "") for d in extracted_docs)
    cleaned_length = sum(len(d.page_content or "") for d in cleaned_docs)

    return {
        "status": "ok",
        "chat_id": chat_id,
        "file": doc.file_name,
        "doc_db_id": doc.id,
        "doc_id": doc.doc_id,
        "raw_length": raw_length,
        "cleaned_length": cleaned_length,
        "num_chunks": len(chunked_docs),
        "num_vectors": len(vectors),
        "collection": collection_name,
    }


# ================================
# 4️⃣ Ask question in a specific chat
# ================================
@router.post("/chats/{chat_id}/ask")
async def ask_in_chat(
    chat_id: int,
    req: AskRequest,
    db: Session = Depends(get_db),
):
    # 0) Check chat exists
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1) Call QA pipeline for this chat (uses per-chat collection)
    try:
        answer = answer_question_for_chat(question, chat_id=chat_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA pipeline error: {e}")

    # 2) Store user + assistant messages in DB
    user_msg = Message(
        chat_id=chat_id,
        role="user",
        content=question,
    )
    assistant_msg = Message(
        chat_id=chat_id,
        role="assistant",
        content=answer,
    )

    db.add(user_msg)
    db.add(assistant_msg)
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    return {
        "chat_id": chat_id,
        "user_message_id": user_msg.id,
        "assistant_message_id": assistant_msg.id,
        "answer": answer,
    }

# ------------------------
# Append this to app/api/routes_chats.py
# ------------------------

from typing import List
from app.models.schemas import MessageOut

# GET chat messages (with simple pagination)
@router.get("/chats/{chat_id}/messages", response_model=List[MessageOut])
def get_chat_messages(
    chat_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Return messages for a chat ordered by timestamp (oldest first).
    Simple pagination via limit & offset.
    """
    # ensure chat exists
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    msgs = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return msgs


from app.models.schemas import DocumentOut

# ================================
# 5️⃣ Get documents for a chat
# ================================
@router.get(
    "/chats/{chat_id}/documents",
    response_model=list[DocumentOut]
)
def get_chat_documents(
    chat_id: int,
    db: Session = Depends(get_db),
):
    # Ensure chat exists
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    docs = (
        db.query(Document)
        .filter(Document.chat_id == chat_id)
        .order_by(Document.uploaded_at.asc())  # 👈 important
        .all()
    )

    return docs

from pydantic import BaseModel
from datetime import datetime

# ================================
# Rename Chat
# ================================

class ChatRename(BaseModel):
    title: str


@router.patch("/chats/{chat_id}", response_model=ChatOut)
def rename_chat(
    chat_id: int,
    payload: ChatRename,
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    new_title = payload.title.strip()
    if not new_title:
        raise HTTPException(status_code=400, detail="Chat title cannot be empty.")

    chat.title = new_title
    chat.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(chat)

    return chat


# ================================
# Delete Chat
# ================================
@router.delete("/chats/{chat_id}")
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    db.delete(chat)
    db.commit()

    return {"status": "ok", "deleted_chat_id": chat_id}


# ================================
# 6️⃣ Generate Chat Summary
# ================================

from app.services.chat_summary import generate_chat_summary

@router.post("/chats/{chat_id}/summary")
def summarize_chat(
    chat_id: int,
    db: Session = Depends(get_db),
):
    # 1) Ensure chat exists
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found.")

    # 2) Fetch all messages (oldest → newest)
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    if not messages:
        raise HTTPException(
            status_code=400,
            detail="Chat has no messages to summarize."
        )

    # 3) Generate summary
    try:
        summary = generate_chat_summary(messages)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summary generation failed: {e}"
        )

    # 4) Return summary (NOT stored)
    return {
        "chat_id": chat_id,
        "summary": summary,
    }
