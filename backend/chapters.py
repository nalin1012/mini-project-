from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional
from datetime import datetime
import re

from database import get_db
from auth import get_current_user
from models import ChapterProgress, User

router = APIRouter(prefix="/api/chapters", tags=["chapters"])


def _slug(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "node"


SYLLABUS: Dict[str, Any] = {
    "Math": {
        "Chapters": {
            "Algebra": {
                "Subtopics": {
                    "Linear Equations": ["Solving for x", "Word Problems"],
                    "Quadratic Equations": ["Factorization", "Discriminant"],
                }
            },
            "Fractions": {
                "Subtopics": {
                    "Basics": ["Equivalent Fractions", "Simplification"],
                    "Operations": ["Add/Subtract", "Multiply/Divide"],
                }
            },
        }
    },
    "Science": {
        "Chapters": {
            "Motion": {
                "Subtopics": {
                    "Kinematics": ["Speed vs Velocity", "Acceleration"],
                    "Graphs": ["Distance-Time", "Velocity-Time"],
                }
            },
            "Energy": {
                "Subtopics": {
                    "Work": ["Work formula", "Units"],
                    "Power": ["Power formula", "Efficiency"],
                }
            },
        }
    },
    "Programming": {
        "Chapters": {
            "Variables": {
                "Subtopics": {
                    "Types": ["Strings", "Numbers"],
                    "Assignment": ["Reassignment", "Expressions"],
                }
            },
            "Loops": {
                "Subtopics": {
                    "for loop": ["range()", "nested loops"],
                    "while loop": ["conditions", "break/continue"],
                }
            },
        }
    },
    "English": {
        "Chapters": {
            "Grammar": {
                "Subtopics": {
                    "Parts of Speech": ["Nouns", "Verbs"],
                    "Tenses": ["Present", "Past"],
                }
            }
        }
    },
    "Aptitude": {
        "Chapters": {
            "Reasoning": {
                "Subtopics": {
                    "Series": ["Number series", "Letter series"],
                    "Analogy": ["Word analogy", "Figure analogy"],
                }
            }
        }
    },
}


class ProgressUpsert(BaseModel):
    subjectId: str
    chapterId: str
    status: str
    percent: int


class SummaryRequest(BaseModel):
    subjectId: str
    chapterId: str
    title: str
    path: Optional[List[str]] = None


def _compute_status(percent: int, saved_status: Optional[str]) -> str:
    if saved_status in {"locked", "in_progress", "done"}:
        return saved_status
    if percent >= 100:
        return "done"
    if percent > 0:
        return "in_progress"
    return "locked"


def _progress_index(rows: List[ChapterProgress]) -> Dict[str, ChapterProgress]:
    return {r.chapter_id: r for r in rows}


def _build_tree(subject: str, progress_rows: List[ChapterProgress]) -> Dict[str, Any]:
    if subject not in SYLLABUS:
        raise HTTPException(status_code=404, detail="Unknown subject")

    idx = _progress_index(progress_rows)

    def node(node_type: str, title: str, subject_id: str, parts: List[str]) -> Dict[str, Any]:
        chapter_id = ".".join([_slug(subject_id)] + [_slug(p) for p in parts])
        row = idx.get(chapter_id)
        percent = int(row.percent_complete) if row else 0
        status_val = _compute_status(percent, row.status if row else None)
        return {
            "id": chapter_id,
            "type": node_type,
            "title": title,
            "subjectId": subject_id,
            "percentComplete": percent,
            "status": status_val,
            "children": [],
        }

    root = node("subject", subject, subject, [subject])
    chapters = SYLLABUS[subject]["Chapters"]

    for chapter_title, chapter_data in chapters.items():
        chapter_node = node("chapter", chapter_title, subject, [subject, chapter_title])

        for subtopic_title, micro_concepts in chapter_data.get("Subtopics", {}).items():
            subtopic_node = node("subtopic", subtopic_title, subject, [subject, chapter_title, subtopic_title])

            for micro in micro_concepts:
                micro_node = node(
                    "micro",
                    micro,
                    subject,
                    [subject, chapter_title, subtopic_title, micro],
                )
                subtopic_node["children"].append(micro_node)

            chapter_node["children"].append(subtopic_node)

        root["children"].append(chapter_node)

    # Simple sequential locking: a chapter is locked until previous is done
    prev_done = True
    for ch in root["children"]:
        if not prev_done:
            ch["status"] = "locked"
            ch["percentComplete"] = 0
        prev_done = ch.get("status") == "done"

    return root


@router.get("")
def get_chapter_map(
    subject: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(ChapterProgress)
        .filter(ChapterProgress.user_id == current_user.id)
        .filter(ChapterProgress.subject_id == subject)
        .all()
    )
    tree = _build_tree(subject, rows)
    return {"subject": subject, "tree": tree}


@router.post("/progress")
def save_progress(
    body: ProgressUpsert,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.percent < 0 or body.percent > 100:
        raise HTTPException(status_code=400, detail="percent must be 0-100")
    status_norm = body.status
    if status_norm not in {"locked", "in_progress", "done"}:
        raise HTTPException(status_code=400, detail="status must be locked|in_progress|done")

    row = (
        db.query(ChapterProgress)
        .filter(ChapterProgress.user_id == current_user.id)
        .filter(ChapterProgress.subject_id == body.subjectId)
        .filter(ChapterProgress.chapter_id == body.chapterId)
        .first()
    )

    if not row:
        row = ChapterProgress(
            user_id=current_user.id,
            subject_id=body.subjectId,
            chapter_id=body.chapterId,
        )
        db.add(row)

    row.status = status_norm
    row.percent_complete = int(body.percent)
    row.last_updated = datetime.utcnow()

    db.commit()

    return {"ok": True}


@router.post("/summary")
def get_summary(
    body: SummaryRequest,
    current_user: User = Depends(get_current_user),
):
    # Uses OpenAI if configured; otherwise provides a simple deterministic fallback.
    try:
        import os
        from openai import OpenAI  # type: ignore

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
            prompt = {
                "topic": body.title,
                "subject": body.subjectId,
                "path": body.path or [],
            }

            sys_msg = (
                "You are an expert study assistant. Return a JSON object with keys: "
                "key_points (array of short bullets), formulas (array), example (string). "
                "If no formulas apply, return an empty formulas array. Keep it concise."
            )

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": f"Summarize: {prompt}"},
                ],
                temperature=0.3,
            )

            text = (resp.choices[0].message.content or "").strip()
            import json

            try:
                data = json.loads(text)
                return {
                    "keyPoints": data.get("key_points") or data.get("keyPoints") or [],
                    "formulas": data.get("formulas") or [],
                    "example": data.get("example") or "",
                }
            except Exception:
                # If the model didn't return JSON, fallback to plain
                return {
                    "keyPoints": [line.strip("- ") for line in text.splitlines() if line.strip()][:8],
                    "formulas": [],
                    "example": "",
                }
    except Exception:
        pass

    return {
        "keyPoints": [
            f"Key idea for {body.title}: understand the definition and typical questions.",
            "Practice 2-3 worked examples to build intuition.",
            "Review common mistakes and how to avoid them.",
        ],
        "formulas": [],
        "example": f"Example: Write one short practice question about {body.title} and solve it step-by-step.",
    }
