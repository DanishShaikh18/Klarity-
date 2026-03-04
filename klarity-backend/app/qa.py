# app/qa.py

from typing import List
from google import genai
import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path, override=True)

from app.embeddings import embed_texts
from app.db.qdrant_client import search_embeddings

# ================================
# 🔑 Gemini API Setup
# ================================
# You can keep your current line here if you hard-coded the key.
# Better long-term: set GEMINI_API_KEY in environment and read it.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not set! Use: setx GEMINI_API_KEY \"your_key\"")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Default global collection (Phase 2)
GLOBAL_COLLECTION_NAME = "klarity_demo"


# ================================
# 🌐 Global QA (old /ask)
# ================================
def answer_question(question: str, top_k: int = 8) -> str:
    """
    Global QA – uses the default collection (klarity_demo).
    Used by your existing /ask endpoint via qa_adapter.
    """
    return _answer_with_collection(
        question=question,
        collection_name=GLOBAL_COLLECTION_NAME,
        top_k=top_k,
    )


# ================================
# 💬 Chat-specific QA (Phase 3)
# ================================
def answer_question_for_chat(question: str, chat_id: int, top_k: int = 8) -> str:
    """
    Chat-specific QA – uses per-chat collection name: klarity_chat_{chat_id}.
    This will be used by /chats/{chat_id}/ask.
    """
    collection_name = f"klarity_chat_{chat_id}"
    return _answer_with_collection(
        question=question,
        collection_name=collection_name,
        top_k=top_k,
    )


# ================================
# 🧠 Shared QA logic for any collection
# ================================
def _answer_with_collection(
    question: str,
    collection_name: str,
    top_k: int = 8,
) -> str:
    """
    Shared logic:
    - embed question
    - search Qdrant in the given collection
    - build context
    - handle "all questions" special case
    - call Gemini
    """
    question = question.strip()
    if not question:
        return "Question is empty."

    # 1) Embed the question
    query_vectors: List[List[float]] = embed_texts([question])
    if not query_vectors:
        return "Failed to generate embedding for the question."

    query_vector = query_vectors[0]

    # 2) Retrieve similar chunks from Qdrant
    results = search_embeddings(
        collection_name=collection_name,
        query_vector=query_vector,
        top_k=top_k,
    )

    if not results:
        return "I couldn't find anything related in the uploaded documents."

    # 3) Collect chunk text
    chunk_texts: List[str] = []
    for r in results:
        payload = r.get("payload") or {}
        text = payload.get("text") or ""
        if text:
            chunk_texts.append(text)

    if not chunk_texts:
        return "Matches found, but no text payload available."

    # 4) Build context string
    context = "\n\n--- CHUNK SEP ---\n\n".join(chunk_texts)

    # ✅ SPECIAL CASE: "all questions" type intent → deterministic extraction
    lower_q = question.lower()
    if (
        "all the questions" in lower_q
        or "all questions" in lower_q
        or "list all questions" in lower_q
        or "give all questions" in lower_q
    ):
        questions = extract_questions_from_context(context)
        if not questions:
            return "Not found in the uploaded documents."

        numbered = [f"{i+1}. {q}" for i, q in enumerate(questions)]
        return "Here are the questions I found in the document:\n" + "\n".join(numbered)

    # 5) Default: Call Gemini with RAG
    answer = call_gemini_rag(question, context)
    return answer


# =======================================
# 🔍 Helper: extract questions from context
# =======================================
def extract_questions_from_context(context: str) -> list[str]:
    """
    Extract lines that look like questions from the retrieved context.
    Very simple heuristic: any line containing "?" and not starting with an answer marker.
    """
    questions: list[str] = []
    seen = set()

    for raw_line in context.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # skip obvious answer/bullet lines
        if line.startswith("➤"):
            continue

        if "?" in line:
            # de-duplicate while preserving order
            if line not in seen:
                seen.add(line)
                questions.append(line)

    return questions


# =======================================
# 🔥 Gemini RAG Call
# =======================================
def call_gemini_rag(question: str, context: str) -> str:
    prompt = f"""
        You are Klarity, an AI assistant.

        You are given extracted text chunks from a document.
        Each chunk is separated by: --- CHUNK SEP ---.

        --------------------------------
        📘 DOCUMENT CONTEXT:
        {context}
        --------------------------------

        ❓ USER QUESTION:
        {question}

        --------------------------------
        🧠 RULES:

        1) Use the document context as the PRIMARY source of information.
        2) You MAY rephrase, explain, reorganize, and clarify the information.
        3) You MAY use general knowledge ONLY to improve clarity and readability and there is any little relevenave take that too
        4) Prioritize the User Question in your answer.
        5) If the document contains partial, implied, or definition-style information
        (for example a heading followed by an explanation),
        you MUST combine and answer it.
        6) ONLY say "Not found in the uploaded documents."
        if the topic is completely absent from all context.


        --------------------------------
        FORMAT RULES (VERY IMPORTANT):

        - Always start with a short overview paragraph (2–3 lines).
        - Use clear section headings using Markdown (##).
        - Separate sections with blank lines.
        - When listing anything, group them logically and use bullet points.
        - Never dump raw lists without headings.
        - Add short one-line explanations where helpful.
        - Prefer readability over compression.

        OUTPUT FORMAT RULES (MANDATORY):

        - Use Markdown headings (##, ###) for sections.
        - Add a blank line before and after each heading.
        - Use bullet points with "-" only.
        - Never inline multiple sections together.
        - Group lists under clear section titles.
        - Prefer readability over brevity.


        End the answer with a short helpful follow-up suggestion if appropriate.

        """


    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"
