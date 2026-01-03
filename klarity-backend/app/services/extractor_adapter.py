# app/services/extractor_adapter.py

from langchain_core.documents import Document as LC_Document
from app.extractor import extract_file_content


def run_extraction(file_path: str) -> list[LC_Document]:
    """
    Call file_extractor.extract_file_content and ALWAYS return list[Document].
    Handles PDF (list[Document]) and DOCX/PPTX (str) outputs.
    """
    result = extract_file_content(file_path)

    # PDF case → already list[Document]
    if isinstance(result, list):
        return result

    # DOCX / PPTX case → string → wrap into a single Document
    if isinstance(result, str):
        return [LC_Document(page_content=result, metadata={"source": file_path})]

    raise TypeError(f"Unexpected extractor output type: {type(result)}")
