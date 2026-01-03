# app/services/embedder_adapter.py

from typing import List, Dict, Any
from langchain_core.documents import Document as LC_Document
from app.embeddings import Embedder

_embedder = Embedder()


def embed_documents(docs: List[LC_Document]) -> List[Dict[str, Any]]:
    """
    Adapter over Embedder.embed_docs
    Input: list[Document] (chunked)
    Output: list[dict] with keys: id, text, embedding, metadata
    """
    return _embedder.embed_docs(docs)
