# app/services/chunking_adapter.py

from typing import List
from langchain_core.documents import Document as LC_Document
from app.chunking import Chunker

_chunker = Chunker()


def chunk_documents(docs: List[LC_Document]) -> List[LC_Document]:
    """
    Adapter over Chunker.chunk
    Input: list[Document] (cleaned)
    Output: list[Document] (chunked)
    """
    return _chunker.chunk(docs)
