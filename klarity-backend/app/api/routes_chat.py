# app/api/routes_chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qa_adapter import answer_question_via_adapter

router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(req: AskRequest):
    question = req.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = answer_question_via_adapter(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA pipeline error: {e}")

    return {"answer": answer}

