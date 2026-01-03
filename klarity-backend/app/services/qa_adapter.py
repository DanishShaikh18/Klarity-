# app/services/qa_adapter.py

from importlib import import_module

def answer_question_via_adapter(question: str) -> str:
    """
    Minimal adapter that imports app.qa and calls answer_question().
    No magic, no auto-discovery, just one clear call.
    """
    module = import_module("app.qa")

    # The function must exist exactly as name "answer_question"
    fn = getattr(module, "answer_question", None)
    if fn is None:
        raise RuntimeError("Function 'answer_question' not found in app.qa")

    return fn(question)
