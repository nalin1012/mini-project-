from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import time

from database import get_db
from models import TutorChat
from auth import get_current_user

router = APIRouter(prefix="/api/tutor", tags=["Tutor"])

SYSTEM_PROMPT = (
    "You are a friendly AI study tutor. Help students understand concepts "
    "clearly. Give step-by-step explanations. Use simple language. "
    "If asked something unrelated to studies, politely redirect."
)


def _safe_reply_fallback(user_text: str) -> str:
    lowered = (user_text or "").strip().lower()
    if not lowered:
        return "Tell me what topic you are studying and what is confusing."

    return (
        "Sure — I can help.\n\n"
        "1) What subject is this (Math/Science/Programming/etc.)?\n"
        "2) What exact part is confusing?\n"
        "3) Share the question or a short excerpt.\n\n"
        "Then I’ll explain step-by-step in simple language."
    )


@router.post("/chat")
def tutor_chat(
    payload: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    messages = payload.get("messages")
    if not isinstance(messages, list):
        raise HTTPException(status_code=400, detail="messages must be a list")

    last_10 = messages[-10:]

    # Persist chat history
    session_id = payload.get("sessionId") or str(uuid.uuid4())
    chat = TutorChat(
        user_id=current_user.id,
        session_id=session_id,
        messages=last_10,
        created_at=int(time.time()),
    )
    db.add(chat)
    db.commit()

    # AI call (fallback-only if OpenAI not configured)
    user_last = ""
    for m in reversed(last_10):
        if isinstance(m, dict) and m.get("role") == "user":
            user_last = str(m.get("content") or "")
            break

    try:
        from openai import OpenAI  # type: ignore

        if not (payload.get("forceFallback") is True):
            api_key = None
            try:
                import os

                api_key = os.getenv("OPENAI_API_KEY")
            except Exception:
                api_key = None

            if api_key:
                client = OpenAI(api_key=api_key)
                chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in last_10:
                    if not isinstance(m, dict):
                        continue
                    role = m.get("role")
                    content = m.get("content")
                    if role in ("user", "assistant") and isinstance(content, str):
                        chat_messages.append({"role": role, "content": content})

                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=chat_messages,
                    temperature=0.4,
                )

                reply = (resp.choices[0].message.content or "").strip()
                return {"reply": reply or _safe_reply_fallback(user_last), "sessionId": session_id}
    except Exception:
        pass

    return {"reply": _safe_reply_fallback(user_last), "sessionId": session_id}


@router.post("/ask")
def tutor_ask(
    payload: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Endpoint for answering specific questions about a topic
    Used by TutorChat component
    """
    message = payload.get("message", "").strip()
    context = payload.get("context", "")
    
    if not message:
        raise HTTPException(status_code=400, detail="message is required")

    # Build the prompt
    system_msg = SYSTEM_PROMPT
    if context:
        system_msg = f"{SYSTEM_PROMPT}\n\nThe student is asking about: {context}"

    try:
        from openai import OpenAI  # type: ignore
        
        api_key = None
        try:
            import os
            api_key = os.getenv("OPENAI_API_KEY")
        except Exception:
            api_key = None

        if api_key:
            client = OpenAI(api_key=api_key)
            
            chat_messages = [{"role": "system", "content": system_msg}]
            chat_messages.append({"role": "user", "content": message})

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_messages,
                temperature=0.4,
            )

            response_text = (resp.choices[0].message.content or "").strip()
            
            # Try to extract explanation and examples from the response
            explanation = None
            examples = []
            
            lines = response_text.split('\n')
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in ['example', 'for instance', 'such as', 'like']):
                    examples.append(line.strip())
            
            return {
                "response": response_text or _safe_reply_fallback(message),
                "explanation": explanation,
                "examples": examples[:3] if examples else None,
            }
    except Exception as e:
        import traceback
        traceback.print_exc()

    # Fallback response
    return {
        "response": _safe_reply_fallback(message),
        "explanation": None,
        "examples": None,
    }
