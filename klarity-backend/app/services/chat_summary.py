# app/services/chat_summary.py

import os
from typing import List
from google import genai

# Create a separate Gemini client for summaries
summary_client = genai.Client(
    api_key=os.getenv("GEMINI_SUMMARY_API_KEY")
)

def build_chat_context(messages: List):
    """
    Convert chat messages into a clean, readable text block
    """
    lines = []

    for msg in messages:
        role = "User" if msg.role == "user" else "Assistant"
        content = msg.content.strip()
        if content:
            lines.append(f"{role}: {content}")

    return "\n\n".join(lines)


def generate_chat_summary(messages: List) -> str:
    """
    Generate a summary for a full chat conversation
    """
    if not messages:
        return "No conversation available to summarize."

    chat_context = build_chat_context(messages)

    prompt = f"""
You are an AI study assistant.

Summarize the following conversation for a student.
The summary should:
- Be well-structured
- Use headings and bullet points where helpful
- Highlight key concepts, definitions, and explanations
- Be concise but complete
- Be written in clear, simple language

Conversation:
----------------
{chat_context}
----------------
"""

    response = summary_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
