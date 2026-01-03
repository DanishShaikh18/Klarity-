# app/services/cleaner_adapter.py

from typing import List
from langchain_core.documents import Document as LC_Document
from app.cleaner import Cleaner

_cleaner = Cleaner()


def clean_documents(blocks: List[LC_Document]) -> List[LC_Document]:
    """
    Adapter over Cleaner.process
    Input: list[Document] (raw blocks)
    Output: list[Document] (cleaned)
    """
    return _cleaner.process(blocks)
