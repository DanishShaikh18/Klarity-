# app/api/routes_upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.utils.file_utils import save_upload_file
from app.services.extractor_adapter import run_extraction
from app.services.cleaner_adapter import clean_documents
from app.services.chunking_adapter import chunk_documents
from app.services.embedder_adapter import embed_documents
from app.db.qdrant_client import upsert_embeddings

router = APIRouter()

COLLECTION_NAME = "klarity_demo"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # 1) Save file
    saved_path = save_upload_file(file)
    if not os.path.exists(saved_path):
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

    # 2) Extract -> list[Document]
    try:
        raw_docs = run_extraction(saved_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {e}")

    if not raw_docs or not isinstance(raw_docs, list):
        raise HTTPException(
            status_code=500,
            detail="Extractor returned no documents or invalid type",
        )

    # 3) Clean docs -> list[Document]
    try:
        cleaned_docs = clean_documents(raw_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning error: {e}")

    if not cleaned_docs:
        raise HTTPException(status_code=500, detail="Cleaner returned no documents")

    # 4) Chunk docs -> list[Document]
    try:
        chunked_docs = chunk_documents(cleaned_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chunking error: {e}")

    if not chunked_docs:
        raise HTTPException(status_code=500, detail="No chunks generated from text")

    # 5) Embed chunks -> list[dict] (each dict: {"id", "text", "embedding", "metadata"})
    try:
        embedded_items = embed_documents(chunked_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    if not embedded_items:
        raise HTTPException(status_code=500, detail="No embeddings generated")

    # 6) Prepare vectors + payloads for Qdrant
    vectors = [item["embedding"] for item in embedded_items]

    payloads = []
    doc_id = os.path.basename(saved_path)

    for item in embedded_items:
        payloads.append(
            {
                "doc_id": doc_id,
                "text": item["text"],
                **(item.get("metadata") or {}),
            }
        )

    # 7) Upsert into Qdrant
    try:
        upsert_embeddings(COLLECTION_NAME, vectors, payloads)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qdrant upsert error: {e}")

    # Just for info: total char lengths
    raw_length = sum(len(getattr(d, "page_content", "") or "") for d in raw_docs)
    cleaned_length = sum(len(getattr(d, "page_content", "") or "") for d in cleaned_docs)

    return {
        "status": "ok",
        "file": os.path.basename(saved_path),
        "path": saved_path,
        "raw_length": raw_length,
        "cleaned_length": cleaned_length,
        "num_chunks": len(chunked_docs),
        "num_vectors": len(vectors),
        "collection": COLLECTION_NAME,
    }
