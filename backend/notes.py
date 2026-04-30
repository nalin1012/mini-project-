from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import os

from auth import get_current_user
from database import get_db
from models import SmartNote, User
from subject_content import (
    get_subject_content,
    get_topic_content,
    generate_subject_flashcards,
    generate_subject_revision,
    generate_subject_notes
)

router = APIRouter(prefix="/api/notes", tags=["notes"])


class GenerateNotesRequest(BaseModel):
    text: str
    title: Optional[str] = None
    subject: Optional[str] = None  # Subject for organizing notes
    sourceType: str = "text"  # text|pdf
    save: bool = False
    noteId: Optional[int] = None
    explainSimply: bool = False


def _fallback_generate(raw: str, subject: Optional[str] = None) -> Dict[str, Any]:
    """Generate fallback notes with subject-specific content if available"""
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    bullets = lines[:12] if lines else ["Add some text and generate notes."]

    # Try to use subject-specific content
    bullet_notes = []
    flashcards = []
    revision_sheet = ""
    
    if subject:
        try:
            subject_data = get_subject_content(subject)
            subject_notes = generate_subject_notes(subject)
            
            # Build bullet notes from subject content
            bullet_notes = [
                {"topic": t["name"], "points": t.get("key_points", [])[:5]}
                for t in subject_notes.get("topics", [])[:3]
            ]
            
            # Get subject flashcards
            flashcards = generate_subject_flashcards(subject, limit=8)
            
            # Build revision sheet
            revision_data = generate_subject_revision(subject)
            revision_sheet = f"""Revision Sheet: {subject}

KEY POINTS:
{chr(10).join([f"- {point}" for point in revision_data.get("key_points", [])[:5]])}

COMMON MISTAKES TO AVOID:
{chr(10).join([f"- {mistake}" for mistake in revision_data.get("common_mistakes", [])[:4]])}

QUICK TIPS:
{chr(10).join([f"- {tip}" for tip in revision_data.get("quick_tips", [])[:3]])}"""
            
            if bullet_notes and flashcards:
                return {
                    "bulletNotes": bullet_notes,
                    "flashcards": flashcards,
                    "revisionSheet": revision_sheet,
                }
        except Exception:
            pass
    
    # Fallback to generic content if subject not found or error
    bullet_notes = [
        {"topic": "Summary", "points": bullets[:8]},
        {"topic": "Key Terms", "points": bullets[8:12] or []},
    ]

    flashcards = []
    for p in bullets[:6]:
        flashcards.append({"q": f"Explain: {p}", "a": p})

    revision_sheet = "\n".join(["Revision Sheet", "", *[f"- {b}" for b in bullets[:12]]])

    return {
        "bulletNotes": bullet_notes,
        "flashcards": flashcards,
        "revisionSheet": revision_sheet,
    }


def _call_ai_generate(raw: str, explain_simply: bool, subject: Optional[str] = None) -> Dict[str, Any]:
    try:
        from openai import OpenAI  # type: ignore

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("missing OPENAI_API_KEY")

        client = OpenAI(api_key=api_key)

        if explain_simply:
            sys_msg = (
                "You rewrite study notes in plain, simple English. "
                "Return JSON with keys: bulletNotes (array of {topic, points}), revisionSheet (string)."
            )
            user_msg = f"Rewrite simply: {raw}"
        else:
            subject_context = f" This is for {subject} subject." if subject else ""
            sys_msg = (
                "You are an expert note taker and educator. Return JSON with keys: "
                "bulletNotes (array of objects {topic, points[]}), "
                "flashcards (array of {q, a} where Q is a clear question testing understanding and A is a concise answer - make these suitable for quiz conversion), "
                "revisionSheet (string with structured revision guide for repeated learning). "
                f"{subject_context} "
                "Create flashcard questions that test concepts, not just definitions. "
                "Prioritize important topics and concepts over trivial details. "
                "Make flashcards educational and useful for exams."
            )
            user_msg = f"Generate comprehensive notes and important concept flashcards from: {raw}\n\nCreate flashcards with clear questions and detailed answers suitable for exam preparation."

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
        )

        text = (resp.choices[0].message.content or "").strip()
        data = json.loads(text)

        if explain_simply:
            return {
                "bulletNotes": data.get("bulletNotes") or data.get("bullet_notes") or [],
                "flashcards": [],
                "revisionSheet": data.get("revisionSheet") or data.get("revision_sheet") or "",
            }

        return {
            "bulletNotes": data.get("bulletNotes") or data.get("bullet_notes") or [],
            "flashcards": data.get("flashcards") or [],
            "revisionSheet": data.get("revisionSheet") or data.get("revision_sheet") or "",
        }
    except Exception:
        if explain_simply:
            base = _fallback_generate(raw, subject)
            return {
                "bulletNotes": base["bulletNotes"],
                "flashcards": [],
                "revisionSheet": base["revisionSheet"],
            }
        return _fallback_generate(raw, subject)


def _generate_revised_notes(raw: str, bullet_notes: List[Dict], subject: Optional[str] = None) -> Dict[str, Any]:
    """Generate revised/condensed notes from original content for spaced repetition"""
    try:
        from openai import OpenAI  # type: ignore

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("missing OPENAI_API_KEY")

        client = OpenAI(api_key=api_key)
        
        subject_context = f" This is for {subject} subject." if subject else ""
        bullets_text = "\n".join([f"- {b['topic']}: {', '.join(b['points'][:3])}" for b in bullet_notes[:5]])
        
        sys_msg = (
            "You are a study expert creating spaced repetition revision notes. "
            "Return JSON with keys: "
            "revisionNotes (array of {topic, summary} for each major concept - concise, 1-2 line summaries), "
            "keyPoints (array of critical points to remember), "
            "commonMistakes (array of common misconceptions to avoid). "
            f"{subject_context}"
        )
        
        user_msg = f"""Create revised/condensed notes for spaced repetition from this content:
Original: {raw[:500]}
Main Topics: {bullets_text}

Focus on what's most important to remember."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
        )

        text = (resp.choices[0].message.content or "").strip()
        data = json.loads(text)
        
        return {
            "revisionNotes": data.get("revisionNotes") or [],
            "keyPoints": data.get("keyPoints") or [],
            "commonMistakes": data.get("commonMistakes") or [],
        }
    except Exception as e:
        # Fallback: Create simple revised notes
        return {
            "revisionNotes": [{"topic": b["topic"], "summary": f"Key points: {', '.join(b['points'][:2])}"} for b in bullet_notes[:3]],
            "keyPoints": [b["points"][0] for b in bullet_notes[:5] if b["points"]],
            "commonMistakes": [],
        }


def _generate_quiz_from_content(raw_content: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generate proper MCQ quiz directly from raw content using AI - BEST QUALITY"""
    try:
        from openai import OpenAI  # type: ignore
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("missing OPENAI_API_KEY")
        
        if not raw_content or len(raw_content) < 50:
            return []
        
        client = OpenAI(api_key=api_key)
        
        # Use only first 3000 chars for context
        content_preview = raw_content[:3000]
        subject_context = f"This content is from {subject}" if subject else ""
        
        sys_msg = (
            "You are an expert exam question designer creating high-quality multiple choice questions. "
            "Generate 6-8 challenging but fair MCQ that test understanding of the material. "
            "Return ONLY a valid JSON array (start with [ directly, no markdown). "
            "Each object must have: "
            '"question" (clear, specific question testing key concept), '
            '"options" (array of exactly 4 realistic, substantive answer choices), '
            '"correct" (index 0-3 of the correct answer), '
            '"explanation" (why this is correct and why others are wrong). '
            f"{subject_context} "
            "Make questions challenging but answerable by someone who studied the material. "
            "Avoid trick questions. Make all options plausible but only one correct. "
            "Test application and understanding, not just memorization."
        )
        
        user_msg = f"""Based on this study material, create 6-8 high-quality exam questions:

{content_preview}

Return ONLY valid JSON array starting with [. No markdown, no code blocks, no other text.
Questions should test understanding of key concepts from the material."""
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.4,  # Slightly higher for variety while keeping quality
        )
        
        text = (resp.choices[0].message.content or "").strip()
        
        if not text:
            return []
        
        # Remove markdown if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            if text.startswith("python"):
                text = text[6:]
        
        # Parse JSON
        import re
        if text.startswith("["):
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                json_match = re.search(r"\[\s*\{.*\}\s*\]", text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    return []
        else:
            return []
        
        # Validate and standardize
        quiz = []
        for q in data:
            if not isinstance(q, dict):
                continue
            
            question = str(q.get("question", "")).strip()
            options = q.get("options", [])
            correct = q.get("correct", 0)
            explanation = str(q.get("explanation", "")).strip()
            
            if not question or len(options) != 4 or not explanation:
                continue
            
            # Validate options
            valid_options = [str(opt).strip() for opt in options if str(opt).strip()]
            if len(valid_options) < 4:
                continue
            
            # Validate correct index
            try:
                correct_idx = int(correct) % 4
            except (ValueError, TypeError):
                correct_idx = 0
            
            quiz.append({
                "question": question[:250],
                "options": valid_options[:4],
                "correct_option": correct_idx,
                "explanation": explanation[:400],
            })
        
        return quiz if len(quiz) >= 4 else []
        
    except Exception as e:
        import logging
        logging.error(f"Quiz generation error: {str(e)}")
        return []


def _generate_quiz_from_flashcards(flashcards: List[Dict], raw_content: str = "", subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generate proper MCQ quiz questions from flashcards and content"""
    try:
        from openai import OpenAI  # type: ignore
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("missing OPENAI_API_KEY")
        
        if not flashcards:
            return []
        
        client = OpenAI(api_key=api_key)
        
        # Prepare flashcard content for AI
        fc_text = "\n".join([f"- {fc['q']} → {fc['a']}" for fc in flashcards[:10]])
        subject_context = f"This is for {subject} subject." if subject else ""
        content_preview = raw_content[:1000] if raw_content else ""
        
        sys_msg = (
            "You are an expert quiz designer creating meaningful multiple choice questions for exam prep. "
            "Create questions that test understanding, not just memorization. "
            "Return ONLY a valid JSON array (no markdown, no code blocks) with 5-8 objects each containing: "
            '"question": clear question text testing a concept, '
            '"options": array of 4 realistic answer choices, '
            '"correct": index (0-3) of correct answer, '
            '"explanation": detailed explanation of why this answer is correct and why others are wrong. '
            f"{subject_context} "
            "Make distractors plausible and educational. Start response with [ directly."
        )
        
        user_msg = f"""Based on this content:
{content_preview if content_preview else fc_text}

Key concepts from flashcards:
{fc_text}

Create 5-8 MCQ questions that test understanding of the main concepts. 
Make options realistic and educational, not generic placeholders.
Return ONLY valid JSON array, no other text."""
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,  # Lower temperature for more consistent format
        )
        
        text = (resp.choices[0].message.content or "").strip()
        
        # Try to parse JSON
        if not text:
            return _fallback_quiz_from_flashcards(flashcards)
            
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        # Parse JSON
        import re
        if text.startswith("["):
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                # Try to find JSON array
                json_match = re.search(r"\[.*\]", text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    return _fallback_quiz_from_flashcards(flashcards)
        else:
            return _fallback_quiz_from_flashcards(flashcards)
        
        # Standardize and validate the response
        quiz = []
        for q in data[:8]:
            if not q.get("question") or not q.get("options"):
                continue
                
            options = q.get("options", [])
            if len(options) < 4:
                continue
                
            quiz.append({
                "question": str(q.get("question", ""))[:200],
                "options": [str(opt)[:100] for opt in options[:4]],
                "correct_option": int(q.get("correct", 0)) % 4,
                "explanation": str(q.get("explanation", ""))[:500],
            })
        
        return quiz if quiz else _fallback_quiz_from_flashcards(flashcards)
    except Exception as e:
        import logging
        logging.error(f"Quiz generation error: {str(e)}")
        return _fallback_quiz_from_flashcards(flashcards)


def _fallback_quiz_from_flashcards(flashcards: List[Dict]) -> List[Dict[str, Any]]:
    """Fallback quiz generation from flashcards - creates realistic MCQ without AI"""
    import random
    
    # Extract key terms and concepts
    concepts = []
    answers = []
    for fc in flashcards:
        q = fc.get("q", "").strip()
        a = fc.get("a", "").strip()
        if q and a:
            concepts.append(q)
            answers.append(a)
    
    if not concepts:
        return []
    
    quiz = []
    
    for i, concept in enumerate(concepts[:6]):
        correct_answer = answers[i]
        
        # Create plausible but incorrect options
        other_answers = [a for j, a in enumerate(answers) if j != i][:3]
        
        # If not enough other answers, create reasonable distractors
        while len(other_answers) < 3:
            if i == 0:
                other_answers.append("A different concept from the material")
            elif i == 1:
                other_answers.append("An alternative or related concept")
            else:
                other_answers.append(f"Another related {concept.split()[0].lower() if concept.split() else 'concept'}")
        
        # Shuffle options and find correct index
        options = [correct_answer] + other_answers[:3]
        random.shuffle(options)
        correct_idx = options.index(correct_answer)
        
        # Create a better question
        question = f"What is the best explanation of {concept}?"
        if "explain" in concept.lower():
            question = concept
        elif "what" in concept.lower():
            question = concept
        elif "define" in concept.lower():
            question = concept.replace("Define", "What is")
        else:
            question = f"Which of the following best describes {concept}?"
        
        quiz.append({
            "question": question[:200],
            "options": [str(opt)[:100] for opt in options],
            "correct_option": correct_idx,
            "explanation": f"The correct answer is: {correct_answer}. This concept is important for understanding the material.",
        })
    
    return quiz


def _convert_subject_to_topics(subject: str):
    """Convert subject content to structured topics format"""
    try:
        from subject_content import get_subject_content
        subject_data = get_subject_content(subject)
        topics = []
        
        if "content" in subject_data:
            for topic_name, content in list(subject_data["content"].items())[:5]:
                topics.append({
                    "title": topic_name,
                    "explanation": content.get("explanation", ""),
                    "keyPoints": content.get("key_points", [])[:5],
                    "formulas": content.get("formulas", [])[:4],
                    "realLifeExample": content.get("real_life", "")
                })
        return topics
    except Exception:
        return []


def _convert_subject_to_flashcards(subject: str):
    """Convert subject content to flashcards format"""
    try:
        from subject_content import generate_subject_flashcards
        return generate_subject_flashcards(subject, limit=12)
    except Exception:
        return []


def _convert_subject_to_revision(subject: str):
    """Convert subject content to revision guide format"""
    try:
        from subject_content import generate_subject_revision
        guide = generate_subject_revision(subject)
        return {
            "importantTopics": guide.get("important_topics", []),
            "commonMistakes": guide.get("common_mistakes", []),
            "quickTips": guide.get("quick_tips", [])
        }
    except Exception:
        return {"importantTopics": [], "commonMistakes": [], "quickTips": []}


async def _read_upload(file: UploadFile) -> Dict[str, str]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    filename = file.filename.lower()
    content = await file.read()

    if filename.endswith(".txt"):
        try:
            text = content.decode("utf-8")
        except Exception:
            text = content.decode("latin-1", errors="ignore")
        return {"text": text, "sourceType": "text"}

    if filename.endswith(".pdf"):
        try:
            try:
                from pypdf import PdfReader  # type: ignore
            except ImportError:
                try:
                    from PyPDF2 import PdfReader  # type: ignore
                except ImportError:
                    raise HTTPException(status_code=400, detail="PDF library not installed. Please install pypdf.")

            import io

            reader = PdfReader(io.BytesIO(content))
            pages = []
            for p in reader.pages:
                text = p.extract_text()
                if text:
                    pages.append(text)
            
            extracted_text = "\n".join(pages).strip()
            if not extracted_text:
                raise HTTPException(status_code=400, detail="No text found in PDF. Please use a text-based PDF.")
            
            return {"text": extracted_text, "sourceType": "pdf"}
        except HTTPException:
            raise
        except Exception as e:
            import logging
            logging.error(f"PDF reading error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")

    raise HTTPException(status_code=400, detail="Only .txt or .pdf supported")


@router.post("/generate")
async def generate_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
    title: Optional[str] = Form(default=None),
    subject: Optional[str] = Form(default=None),
    save: Optional[bool] = Form(default=False),
    noteId: Optional[int] = Form(default=None),
    explainSimply: Optional[bool] = Form(default=False),
):
    # Supports multipart/form-data only (file or text field). Keeps API surface simple for the frontend.
    raw = ""
    source_type = "text"

    if file is not None:
        payload = await _read_upload(file)
        raw = payload["text"]
        source_type = payload["sourceType"]
    elif text is not None:
        raw = text
        source_type = "text"
    else:
        raise HTTPException(status_code=400, detail="Provide file or text")

    raw = (raw or "").strip()
    if len(raw) < 10:
        raise HTTPException(status_code=400, detail="Text is too short")

    generated = _call_ai_generate(raw, bool(explainSimply), subject)
    
    # Generate quiz questions directly from content (PRIMARY METHOD for best quality)
    # Falls back to flashcard method if content-based generation fails
    quiz_questions = _generate_quiz_from_content(raw, subject)
    if not quiz_questions:
        # Fallback to flashcard-based generation if direct method fails
        quiz_questions = _generate_quiz_from_flashcards(generated.get("flashcards", []), raw, subject)

    saved_id: Optional[int] = None
    if save:
        note: Optional[SmartNote] = None
        if noteId is not None:
            note = (
                db.query(SmartNote)
                .filter(SmartNote.id == noteId)
                .filter(SmartNote.user_id == current_user.id)
                .first()
            )

        if not note:
            note = SmartNote(
                user_id=current_user.id,
                subject=subject,
                title=(title or "Untitled Note").strip() or "Untitled Note",
                source_type=source_type,
                raw_content=raw,
                created_at=datetime.utcnow(),
            )
            db.add(note)

        note.subject = subject
        note.bullet_notes = generated.get("bulletNotes")
        note.flashcards = generated.get("flashcards")
        note.revision_sheet = generated.get("revisionSheet")
        note.source_type = source_type
        note.raw_content = raw
        
        # Generate revised notes for spaced repetition
        revised = _generate_revised_notes(raw, generated.get("bulletNotes", []), subject)
        note.revised_notes = revised

        db.commit()
        db.refresh(note)
        saved_id = note.id

    return {
        **generated,
        "quiz": quiz_questions,
        "noteId": saved_id,
        "sourceType": source_type,
        "subject": subject,
        "title": title or "Untitled Note",
    }


@router.get("")
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notes = (
        db.query(SmartNote)
        .filter(SmartNote.user_id == current_user.id)
        .order_by(SmartNote.created_at.desc())
        .all()
    )

    return {
        "notes": [
            {
                "id": n.id,
                "title": n.title,
                "subject": n.subject,
                "sourceType": n.source_type,
                "createdAt": n.created_at.isoformat() if n.created_at else None,
            }
            for n in notes
        ]
    }


@router.get("/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(SmartNote)
        .filter(SmartNote.id == note_id)
        .filter(SmartNote.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": note.id,
        "title": note.title,
        "subject": note.subject,
        "sourceType": note.source_type,
        "rawContent": note.raw_content,
        "bulletNotes": note.bullet_notes or [],
        "flashcards": note.flashcards or [],
        "revisionSheet": note.revision_sheet or "",
        "revisionNotes": note.revised_notes or {},
        "createdAt": note.created_at.isoformat() if note.created_at else None,
    }


# Subject-specific notes endpoint with comprehensive content
SUBJECT_CONTENT = {
    "Math": """
COMPREHENSIVE MATHEMATICS REVISION GUIDE

1. FRACTIONS & DECIMALS
   - Simplifying fractions: Find GCD and divide both numerator and denominator
   - Converting decimals to fractions: Place value over powers of 10
   - Adding/Subtracting: Find LCM of denominators, then combine
   - Multiplying: Multiply numerators and denominators separately
   - Dividing: Multiply by reciprocal of divisor
   - Comparing: Convert to common denominator or convert to decimals
   - Decimal operations: Align decimal points, perform operation
   - Percentage: Express as fraction with denominator 100
   
2. ALGEBRA
   - Linear equations: ax + b = c, solve by isolating x
   - Quadratic equations: ax² + bx + c = 0, use factoring or quadratic formula
   - Systems of equations: Substitution or elimination method
   - Inequalities: Same rules as equations, flip sign when multiplying/dividing by negative
   - Functions: f(x) = y, domain is input values, range is output values
   - Graphing: Plot points, find slope (rise/run), y-intercept
   - Exponents: aⁿ × aᵐ = aⁿ⁺ᵐ, (aⁿ)ᵐ = aⁿᵐ, a⁰ = 1
   - Radicals: √(ab) = √a × √b, rationalize denominators
   
3. GEOMETRY
   - Triangles: Sum of angles = 180°, Pythagorean theorem a² + b² = c²
   - Area formulas: Rectangle = lw, Triangle = ½bh, Circle = πr²
   - Volume formulas: Cube = s³, Cylinder = πr²h, Sphere = ⁴⁄₃πr³
   - Perimeter: Sum of all sides, Circle circumference = 2πr
   - Congruence: Same size and shape (SSS, SAS, ASA)
   - Similarity: Same shape, proportional sides
   - Coordinate geometry: Distance formula, midpoint formula, slope
   
4. TRIGONOMETRY
   - SOH-CAH-TOA: sin = opposite/hypotenuse, cos = adjacent/hypotenuse, tan = opposite/adjacent
   - Special angles: 0°, 30°, 45°, 60°, 90° (memorize key values)
   - Unit circle: Radius 1, helps find trig values for any angle
   - Pythagorean identity: sin²θ + cos²θ = 1
   - Angle sum formulas: sin(A+B) = sinAcosB + cosAsinB
   - Solving triangles: Use law of sines or law of cosines
   
5. CALCULUS BASICS
   - Limits: Value function approaches as x approaches a point
   - Derivatives: Rate of change, slope of tangent line
   - Power rule: d/dx(xⁿ) = n×xⁿ⁻¹
   - Integrals: Reverse of derivatives, area under curve
   - Fundamental theorem: Derivative and integral are inverse operations
   
6. STATISTICS & PROBABILITY
   - Mean: Sum of all values divided by count
   - Median: Middle value when ordered, Q2 of box plot
   - Mode: Most frequently occurring value
   - Standard deviation: Measures spread of data from mean
   - Probability: Number of favorable outcomes / total outcomes
   - Normal distribution: Bell curve, 68% within 1 SD, 95% within 2 SD
""",
    
    "Science": """
COMPREHENSIVE SCIENCE REVISION GUIDE

1. PHYSICS
   - Motion: Speed = distance/time, Velocity = displacement/time with direction
   - Acceleration: Change in velocity over time, a = (v-u)/t
   - Force: F = ma (Newton's second law), measured in Newtons
   - Work: W = Force × Distance, measured in Joules
   - Energy: Kinetic = ½mv², Potential = mgh, conserved in closed systems
   - Waves: Wavelength × Frequency = Speed, amplitude = height
   - Electricity: Voltage = current × resistance (Ohm's law), Power = VI
   - Magnetism: Opposite poles attract, same poles repel
   - Pressure: P = Force/Area, increases with depth in fluids
   
2. CHEMISTRY
   - Atomic structure: Protons (positive) + Neutrons = nucleus, Electrons (negative) orbit
   - Atomic number: Number of protons (defines element)
   - Atomic mass: Protons + Neutrons
   - Ions: Charged atoms (cations positive, anions negative)
   - Chemical bonds: Ionic (transfer electrons), Covalent (share electrons)
   - Molecular weight: Sum of atomic weights of all atoms
   - Reactions: Reactants → Products, conserve mass and energy
   - Oxidation-reduction: Oxidation = lose electrons, Reduction = gain electrons
   - pH scale: 0-7 acidic, 7 neutral, 7-14 basic
   - Periodic table: Organized by atomic number, similar properties in columns
   
3. BIOLOGY
   - Cell structure: Nucleus (DNA), Mitochondria (energy), Ribosomes (protein)
   - Photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂ (glucose and oxygen)
   - Cellular respiration: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy (ATP)
   - DNA: Double helix, carries genetic information with A-T and G-C base pairs
   - Genetics: Mendel's laws, dominant and recessive traits
   - Evolution: Natural selection, survival of the fittest, adaptation
   - Ecosystems: Energy flows, food chains, nutrient cycles
   - Classification: Kingdom, Phylum, Class, Order, Family, Genus, Species
   - Immune system: White blood cells fight pathogens
   
4. EARTH SCIENCE
   - Plate tectonics: Continental drift, transform and convergent boundaries
   - Earthquakes: Caused by tectonic movement, measured on Richter scale
   - Volcanoes: Magma erupts from mantle, types: shield, cinder, composite
   - Rock cycle: Igneous, Sedimentary, Metamorphic rocks transform
   - Weather: Caused by uneven solar heating, creates pressure differences
   - Atmosphere: Layers (troposphere, stratosphere, mesosphere, thermosphere)
   - Water cycle: Evaporation, Condensation, Precipitation, Collection
   - Climate: Long-term weather patterns, influenced by latitude and ocean currents
   
5. OPTICS
   - Light: Travels in straight lines at 3×10⁸ m/s in vacuum
   - Reflection: Angle of incidence = angle of reflection
   - Refraction: Light bends when entering different medium, n₁sinθ₁ = n₂sinθ₂
   - Lenses: Convex (converging), Concave (diverging)
   - Focus: Point where light rays meet or appear to originate
   - Lens equation: 1/f = 1/u + 1/v
""",

    "Programming": """
COMPREHENSIVE PROGRAMMING REVISION GUIDE

1. FUNDAMENTALS
   - Variables: Named containers storing values (int, float, string, bool)
   - Data types: Integers (whole numbers), Floats (decimals), Strings (text)
   - Operators: Arithmetic (+, -, *, /, %), Comparison (==, !=, <, >), Logical (and, or, not)
   - Type casting: Convert between types (int(), str(), float())
   - Constants: Values that don't change (use UPPER_CASE naming)
   
2. CONTROL FLOW
   - If-else: Conditional execution based on boolean conditions
   - Switch/case: Multiple conditions, cleaner than many if-else
   - Loops: For (fixed iterations), While (condition-based), Do-while
   - Break: Exit loop immediately
   - Continue: Skip to next iteration
   - Nested loops: Loops inside loops
   
3. FUNCTIONS
   - Definition: Code block performing specific task
   - Parameters: Inputs to function
   - Return value: Output from function
   - Scope: Local (inside function), Global (entire program)
   - Recursion: Function calling itself with base case
   - Closures: Inner function accessing outer function variables
   
4. DATA STRUCTURES
   - Arrays/Lists: Ordered, indexed collection (0-based indexing)
   - Strings: Sequence of characters, immutable in most languages
   - Dictionaries/Maps: Key-value pairs, unordered
   - Sets: Unique values, unordered
   - Tuples: Immutable ordered collection
   - Stacks: LIFO (Last In, First Out)
   - Queues: FIFO (First In, First Out)
   
5. OBJECT-ORIENTED PROGRAMMING
   - Classes: Blueprint for objects
   - Objects: Instances of classes with properties and methods
   - Encapsulation: Hide internal details, expose interface
   - Inheritance: Subclass inherits from superclass
   - Polymorphism: Same interface, different implementations
   - Abstraction: Define what object does, not how
   
6. ALGORITHMS
   - Sorting: Bubble, Selection, Insertion, Merge, Quick (compare implementations)
   - Searching: Linear (check each item), Binary (divide and conquer)
   - Time complexity: Big O notation (O(1), O(n), O(n²), O(nlogn))
   - Space complexity: Memory used by algorithm
   - Greedy algorithms: Make locally optimal choice at each step
   
7. WEB DEVELOPMENT
   - HTML: Structure (tags like <div>, <p>, <a>)
   - CSS: Styling (selectors, properties, media queries)
   - JavaScript: Client-side interactivity (DOM manipulation, events)
   - APIs: Request-response pattern (REST, JSON, HTTP methods)
   - Databases: Store persistent data (SQL, NoSQL)
   - Frameworks: React, Vue (frontend), Express, Django (backend)
   
8. DEBUGGING
   - Print/log statements: Track variable values
   - Breakpoints: Pause execution to inspect state
   - Error handling: Try-catch blocks to handle exceptions
   - Unit tests: Test individual functions
   - Common bugs: Null pointer, off-by-one, infinite loops
""",

    "English": """
COMPREHENSIVE ENGLISH REVISION GUIDE

1. READING COMPREHENSION
   - Main idea: Central point of passage
   - Supporting details: Facts and examples that support main idea
   - Inference: Drawing conclusions from text (read between lines)
   - Context clues: Use surrounding words to understand unknown words
   - Fact vs opinion: Fact is verifiable, opinion is personal belief
   - Summarization: Brief statement of key points
   - Author's purpose: Why author wrote passage (inform, entertain, persuade)
   - Tone: Author's attitude (serious, humorous, sarcastic, formal)
   
2. WRITING ESSAYS
   - Thesis statement: Main argument of essay (specific, arguable, narrow)
   - Introduction: Hook reader, provide background, state thesis
   - Body paragraphs: Topic sentence, supporting evidence, explanation
   - Topic sentences: Introduce main idea of each paragraph
   - Evidence: Quotes, examples, statistics supporting claims
   - Transitions: Connect ideas between sentences and paragraphs
   - Conclusion: Restate thesis, summarize main points, broader implications
   - Paragraph structure: Topic-Evidence-Analysis (TEA) or similar
   
3. GRAMMAR & MECHANICS
   - Parts of speech: Nouns, Verbs, Adjectives, Adverbs, Prepositions, Conjunctions
   - Sentence types: Simple (one clause), Compound (two independent clauses), Complex (independent + dependent)
   - Run-on sentences: Join with conjunction or semicolon
   - Fragments: Incomplete sentences, add subject or verb
   - Subject-verb agreement: Singular subject + singular verb
   - Tense consistency: Maintain same tense throughout
   - Comma usage: Separate items, join clauses, set off information
   - Semicolons: Join independent clauses or separate complex items
   - Apostrophes: Show possession (s's) or contractions (don't)
   
4. VOCABULARY & WORD STUDY
   - Word roots: Latin/Greek foundations of words
   - Prefixes: Attached to beginning (un-, re-, pre-)
   - Suffixes: Attached to end (-tion, -able, -ness)
   - Synonyms: Words with similar meanings
   - Antonyms: Words with opposite meanings
   - Homonyms: Words that sound same but different meaning
   - Connotation: Emotional association of word
   - Denotation: Literal dictionary definition
   
5. LITERATURE ANALYSIS
   - Themes: Universal ideas/messages in work
   - Characters: Protagonist (main character), Antagonist (opposition)
   - Character development: How character changes throughout story
   - Plot: Exposition, Rising action, Climax, Falling action, Resolution
   - Setting: Time and place of story
   - Symbolism: Objects/concepts representing deeper meaning
   - Conflict: Internal (within self), External (against external force)
   - Point of view: First person (I), Second person (you), Third person (he/she/it)
   - Figurative language: Metaphor, Simile, Personification, Hyperbole
""",

    "Aptitude": """
COMPREHENSIVE APTITUDE REVISION GUIDE

1. LOGICAL REASONING
   - Syllogisms: Two premises → one conclusion
   - Analogies: A:B :: C:D (relationship pattern matching)
   - Patterns: Number, alphabetic, visual sequences (find rule)
   - Blood relations: Family connections, draw diagrams
   - Direction sense: North, South, East, West, find positions
   - Coding-decoding: Substitute letters/numbers based on rules
   - Venn diagrams: Set relationships and overlaps
   
2. QUANTITATIVE APTITUDE
   - Speed, time, distance: Distance = Speed × Time
   - Work rate: Combined work = 1/A + 1/B work units per hour
   - Percentage: (Part/Whole) × 100, increase/decrease calculations
   - Ratio and proportion: a:b = c:d, cross multiply
   - Simple interest: SI = (P × R × T)/100
   - Compound interest: A = P(1 + r/100)ⁿ
   - Profit and loss: Profit% = ((SP-CP)/CP) × 100
   - Average: Sum of values / Number of values
   
3. DATA INTERPRETATION
   - Line graphs: Track trends over time
   - Bar charts: Compare values across categories
   - Pie charts: Show proportions of whole
   - Tables: Organize numerical data
   - Interpretation: Read values, calculate ratios, identify trends
   - Comparisons: Find highest/lowest, differences
   
4. CRITICAL THINKING & PROBLEM SOLVING
   - Root cause analysis: Find underlying problem, not symptom
   - Hypothesis: Testable prediction
   - Inference: Conclusion based on evidence
   - Assumption: Unstated belief
   - Argument validity: Premises support conclusion
   
5. SPATIAL REASONING
   - Rotation: Mental rotation of objects 2D/3D
   - Reflection: Mirror image of objects
   - Folding: Visualize unfolded 3D object
   - Hidden figures: Find patterns within complex drawings
   - Matrix reasoning: Identify pattern in 3×3 grids
   - Cubes: Unfolded cube patterns
""",

    "Study Skills": """
COMPREHENSIVE STUDY SKILLS REVISION GUIDE

1. TIME MANAGEMENT
   - Pomodoro technique: 25 min focused work + 5 min break
   - Eisenhower matrix: Urgent/Important → prioritize tasks
   - Weekly schedule: Allocate study time for each subject
   - Break study into sessions: 25-50 minutes for focus
   - Avoid procrastination: Break large tasks into smaller chunks
   - Track time: See where time goes, adjust schedule
   
2. NOTE-TAKING METHODS
   - Cornell method: Divide page (notes right, cues left, summary bottom)
   - Mind mapping: Central idea with branches of related concepts
   - Outline: Hierarchical organization with main points and sub-points
   - Concept mapping: Show relationships between concepts
   - Two-column: Question column and answer column
   - Active listening: Focus, write key ideas not word-for-word
   
3. MEMORY TECHNIQUES
   - Mnemonics: Acronyms or phrases to remember lists
   - Method of loci: Associate items with locations
   - Spaced repetition: Review material at increasing intervals (1d, 3d, 1w, 1m)
   - Chunking: Group information into meaningful units
   - Elaboration: Connect new info to existing knowledge
   - Visualization: Create mental images
   - Teach back: Explain concept to someone else
   
4. EXAM PREPARATION
   - Practice tests: Take full-length tests under conditions
   - Review mistakes: Understand why you got it wrong
   - Time management during exam: Allocate time per question
   - Read carefully: Understand what question asks
   - Eliminate options: Rule out obviously wrong answers
   - Double-check: Review answers before submission
   - Positive thinking: Confidence affects performance
   
5. READING STRATEGIES
   - SQ3R: Survey, Question, Read, Recite, Review
   - Skimming: Quick overview to get gist
   - Scanning: Look for specific information
   - Active reading: Highlight, annotate, question
   - Vocabulary building: Learn new words daily
   - Read different materials: Textbooks, articles, journals
   
6. GROUP STUDY
   - Find motivated partners: Quality over quantity
   - Set agenda: Define what to cover
   - Explain to others: Deepen understanding
   - Discuss difficult concepts: Get alternative perspectives
   - Quiz each other: Test knowledge
   - Balance: Group study + individual study
   
7. HEALTHY STUDYING
   - Sleep: 7-8 hours for memory consolidation
   - Exercise: Improves focus and mood
   - Nutrition: Stable blood sugar, brain fuel
   - Hydration: Drink water throughout day
   - Breaks: Rest eyes, stretch, breathe
   - Minimize distractions: Phone away, quiet space
"""
}

def _generate_from_subject_content(content: str, subject: str) -> Dict[str, Any]:
    """Generate notes structure from subject content with real flashcards"""
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    
    # Extract sections (lines starting with numbers like "1.", "2.", etc.)
    sections = []
    current_section = None
    
    for line in lines:
        if line and line[0].isdigit() and '.' in line[:3]:
            # This is a section header
            current_section = {"topic": line, "points": []}
            sections.append(current_section)
        elif current_section and line and not (line[0].isdigit() and '.' in line[:3]):
            # This is a point under the current section
            if line.startswith('-'):
                current_section["points"].append(line[1:].strip())
            else:
                current_section["points"].append(line)
    
    # Build bullet notes from sections
    bullet_notes = [
        {"topic": s["topic"], "points": s["points"][:8]}  # First 8 points per section
        for s in sections[:5]  # Take first 5 sections
    ]
    
    # Create meaningful flashcards from key points - NOT generic ones
    flashcards = []
    seen_qs = set()
    
    for section in sections:
        topic = section["topic"]
        # Extract the topic name (e.g., "1. FRACTIONS" -> "Fractions")
        topic_name = topic.split(".")[-1].strip() if "." in topic else topic
        
        if section["points"]:
            # Create question from first point
            first_point = section["points"][0]
            q = f"What is {topic_name}?"
            a = first_point[:100]  # First 100 chars of the explanation
            
            if q not in seen_qs:
                flashcards.append({"q": q, "a": a})
                seen_qs.add(q)
            
            # Create second question from second point if exists
            if len(section["points"]) > 1:
                second_point = section["points"][1]
                q2 = f"How do you {second_point[:50]}...?"
                a2 = second_point[:100]
                
                if q2 not in seen_qs:
                    flashcards.append({"q": q2, "a": a2})
                    seen_qs.add(q2)
    
    # Ensure we have at least some flashcards
    if not flashcards:
        flashcards = [
            {"q": "What are the main topics?", "a": " | ".join([s["topic"] for s in sections[:3]])},
        ]
    
    # Create revision sheet with all content
    revision_sheet = f"REVISION: {subject}\n\n" + content
    
    return {
        "bulletNotes": bullet_notes if bullet_notes else [{"topic": "Overview", "points": lines[:10]}],
        "flashcards": flashcards[:8],  # Return up to 8 flashcards
        "revisionSheet": revision_sheet,
    }


@router.get("/subject/{subject}")
async def get_notes_for_subject(
    subject: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get or generate notes for a specific subject"""
    # Try to find existing notes for this subject
    note = (
        db.query(SmartNote)
        .filter(SmartNote.user_id == current_user.id)
        .filter(SmartNote.title.ilike(f"%{subject}%"))
        .order_by(SmartNote.created_at.desc())
        .first()
    )
    
    if note:
        return {
            "bulletNotes": note.bullet_notes or [],
            "flashcards": note.flashcards or [],
            "revisionSheet": note.revision_sheet or "",
            "source": "saved",
        }
    
    # Generate default notes from subject content
    content = SUBJECT_CONTENT.get(subject, f"Study material for {subject}")
    generated = _generate_from_subject_content(content, subject)
    
    return {
        **generated,
        "source": "generated",
    }


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(SmartNote)
        .filter(SmartNote.id == note_id)
        .filter(SmartNote.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"ok": True}


# ============================================================================
# STRUCTURED LEARNING CONTENT ENDPOINTS (Study Notebook System)
# ============================================================================

# Comprehensive topic-based content for each subject
STRUCTURED_TOPICS = {
    "Math": [
        {
            "title": "Laws of Motion",
            "explanation": "Motion describes how objects move under forces. The laws of motion form the foundation of classical mechanics.",
            "keyPoints": [
                "Force = mass × acceleration (F = ma)",
                "Every action has an equal and opposite reaction",
                "An object in motion stays in motion unless acted upon by a force",
                "Net force determines acceleration direction"
            ],
            "formulas": [
                "F = m × a (Newton's Second Law)",
                "F₁ = -F₂ (Newton's Third Law)",
                "a = Δv / Δt (Acceleration)"
            ],
            "realLifeExample": "Pushing a shopping cart requires force. The harder you push (larger force), the faster it accelerates."
        },
        {
            "title": "Work and Energy",
            "explanation": "Work is the transfer of energy through a force, and energy is the capacity to do work.",
            "keyPoints": [
                "Work = Force × Distance (when force is parallel to motion)",
                "Energy cannot be created or destroyed, only transformed",
                "Kinetic energy depends on mass and velocity",
                "Potential energy depends on height and gravity"
            ],
            "formulas": [
                "W = F × d × cos(θ) (Work)",
                "KE = ½ × m × v² (Kinetic Energy)",
                "PE = m × g × h (Potential Energy)",
                "Total Energy = KE + PE (Conservation)"
            ],
            "realLifeExample": "Lifting a book stores potential energy. Dropping it converts PE to KE as it falls."
        },
        {
            "title": "Projectile Motion",
            "explanation": "Motion of an object thrown or projected into the air, affected by gravity and initial velocity.",
            "keyPoints": [
                "Horizontal velocity remains constant",
                "Vertical motion is independent of horizontal motion",
                "Gravity affects only vertical motion",
                "Path forms a parabola"
            ],
            "formulas": [
                "Horizontal: x = v₀ₓ × t",
                "Vertical: y = v₀ᵧ × t - ½gt²",
                "Range = (v₀² × sin(2θ)) / g"
            ],
            "realLifeExample": "A basketball shot follows a parabolic path due to gravity pulling it downward while moving horizontally."
        }
    ],
    "Science": [
        {
            "title": "Laws of Motion",
            "explanation": "Newton's three laws describe how objects move and interact with forces.",
            "keyPoints": [
                "First Law: An object at rest stays at rest unless acted upon",
                "Second Law: Acceleration is proportional to force (F = ma)",
                "Third Law: For every action, there's an equal opposite reaction",
                "Inertia is the resistance to change in motion"
            ],
            "formulas": [
                "F = m × a",
                "Weight = m × g",
                "Momentum = m × v"
            ],
            "realLifeExample": "A car needs force to accelerate. The heavier the car, the more force needed to achieve the same acceleration."
        },
        {
            "title": "Photosynthesis",
            "explanation": "The process by which plants convert light energy into chemical energy stored in glucose.",
            "keyPoints": [
                "Occurs in chloroplasts of plant cells",
                "Uses carbon dioxide and water",
                "Produces glucose and oxygen",
                "Requires sunlight as energy source",
                "Two stages: Light reactions and Calvin cycle"
            ],
            "formulas": [
                "6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂"
            ],
            "realLifeExample": "Plants capture sunlight to make their own food. This is why plants need sunlight to grow."
        },
        {
            "title": "Atomic Structure",
            "explanation": "The composition of atoms: protons, neutrons, and electrons arranged in specific patterns.",
            "keyPoints": [
                "Nucleus contains protons (positive) and neutrons (neutral)",
                "Electrons (negative) orbit the nucleus",
                "Atomic number = number of protons",
                "Mass number = protons + neutrons",
                "Electrons determine chemical properties"
            ],
            "formulas": [
                "Atomic Number = Number of Protons",
                "Mass Number = Protons + Neutrons",
                "Number of Electrons = Protons (for neutral atoms)"
            ],
            "realLifeExample": "Carbon-12 has 6 protons, 6 neutrons, and 6 electrons. This makes it stable and forms the basis of all life."
        }
    ],
    "Programming": [
        {
            "title": "Variables and Data Types",
            "explanation": "Variables are containers for storing data. Different data types represent different kinds of information.",
            "keyPoints": [
                "Variables store data in memory",
                "Data types: int, float, string, boolean",
                "Naming convention: lowercase with underscores (snake_case)",
                "Type casting converts between types",
                "Variables must be declared before use (in typed languages)"
            ],
            "formulas": [
                "variable_name = value",
                "type_name(variable) # Type casting",
                "len(variable) # Get length"
            ],
            "realLifeExample": "age = 25 stores the number 25. name = 'John' stores text. age is an integer, name is a string."
        },
        {
            "title": "Loops and Iteration",
            "explanation": "Loops repeat a block of code multiple times, useful for processing collections of data.",
            "keyPoints": [
                "For loops iterate a fixed number of times",
                "While loops continue until condition is false",
                "Break exits the loop early",
                "Continue skips current iteration",
                "Nested loops: loops within loops"
            ],
            "formulas": [
                "for i in range(10): # Repeat 10 times",
                "while condition: # Repeat while true",
                "for item in list: # Iterate through items"
            ],
            "realLifeExample": "A for loop can process each student in a class. A while loop can continue until a user enters the correct password."
        },
        {
            "title": "Functions",
            "explanation": "Functions are reusable blocks of code that perform specific tasks.",
            "keyPoints": [
                "Functions reduce code repetition",
                "Parameters are inputs to functions",
                "Return value is the output",
                "Scope: Local vs Global variables",
                "Function names should be descriptive"
            ],
            "formulas": [
                "def function_name(parameters):",
                "    return value",
                "function_name(arguments)"
            ],
            "realLifeExample": "A function to calculate BMI takes weight and height as parameters and returns the BMI value."
        }
    ],
    "English": [
        {
            "title": "Parts of Speech",
            "explanation": "Words are categorized into different types based on their function in a sentence.",
            "keyPoints": [
                "Nouns: name people, places, things",
                "Verbs: action or state words",
                "Adjectives: describe nouns",
                "Adverbs: describe verbs, adjectives",
                "Pronouns: replace nouns (he, she, it)"
            ],
            "formulas": [
                "Sentence = Subject (Noun) + Predicate (Verb + Object)",
                "Example: The cat (noun) runs (verb) quickly (adverb)"
            ],
            "realLifeExample": "'She quickly ate the delicious apple.' She=pronoun, quickly=adverb, ate=verb, delicious=adjective, apple=noun"
        },
        {
            "title": "Sentence Structure",
            "explanation": "The arrangement of words and phrases to create meaningful sentences.",
            "keyPoints": [
                "Simple: One independent clause",
                "Compound: Two independent clauses",
                "Complex: One independent + dependent clause",
                "Subject-Verb agreement is essential",
                "Word order affects meaning"
            ],
            "formulas": [
                "Simple: She reads books.",
                "Compound: She reads books, and he writes stories.",
                "Complex: She reads books that are interesting."
            ],
            "realLifeExample": "'I read because I love stories' is complex: 'I read' is independent, 'because I love stories' is dependent."
        }
    ],
    "Aptitude": [
        {
            "title": "Logical Reasoning",
            "explanation": "Using logic and analytical skills to solve problems systematically.",
            "keyPoints": [
                "Identify patterns in sequences",
                "Use deductive reasoning (specific from general)",
                "Use inductive reasoning (general from specific)",
                "Eliminate impossible options",
                "Check your assumptions"
            ],
            "formulas": [
                "If All X are Y, and All Y are Z, then All X are Z",
                "Pattern Recognition: Find what changes and what stays same",
                "Probability: Favorable outcomes / Total outcomes"
            ],
            "realLifeExample": "Series: 2, 4, 6, 8, ? Answer is 10 (add 2 each time). Pattern recognition helps solve puzzles quickly."
        },
        {
            "title": "Data Interpretation",
            "explanation": "Understanding and analyzing data from charts, graphs, and tables to draw conclusions.",
            "keyPoints": [
                "Read axes carefully on graphs",
                "Calculate percentages and ratios",
                "Compare values accurately",
                "Identify trends and anomalies",
                "Consider context and scale"
            ],
            "formulas": [
                "Percentage = (Part/Whole) × 100",
                "Ratio = Part : Part or Part : Whole",
                "Average = Sum / Count",
                "Growth Rate = (New - Old) / Old × 100"
            ],
            "realLifeExample": "A bar chart shows sales: Jan=100, Feb=150. Growth = (150-100)/100 × 100 = 50% increase."
        }
    ]
}

# Structured flashcards for each subject
STRUCTURED_FLASHCARDS = {
    "Math": [
        {"front": "Newton's Second Law", "back": "F = ma (Force equals mass times acceleration)"},
        {"front": "Newton's Third Law", "back": "For every action, there is an equal and opposite reaction"},
        {"front": "Kinetic Energy Formula", "back": "KE = ½ × m × v² (half mass times velocity squared)"},
        {"front": "Potential Energy Formula", "back": "PE = mgh (mass times gravity times height)"},
        {"front": "Work Formula", "back": "W = F × d × cos(θ) (force times distance times cosine of angle)"},
        {"front": "Speed Formula", "back": "Speed = Distance / Time"},
        {"front": "Acceleration", "back": "a = Δv / Δt (change in velocity divided by change in time)"},
        {"front": "What is Inertia?", "back": "The tendency of an object to resist changes in motion"}
    ],
    "Science": [
        {"front": "Photosynthesis Equation", "back": "6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂"},
        {"front": "What is ATP?", "back": "Adenosine Triphosphate - the energy currency of cells"},
        {"front": "DNA Base Pairs", "back": "Adenine pairs with Thymine, Guanine pairs with Cytosine"},
        {"front": "Mitochondria Function", "back": "Powerhouse of the cell - produces energy (ATP)"},
        {"front": "Osmosis", "back": "Movement of water across a semipermeable membrane toward higher solute concentration"},
        {"front": "What are Prokaryotes?", "back": "Single-celled organisms without a nucleus (bacteria)"},
        {"front": "Valence Electrons", "back": "Electrons in the outermost shell that determine chemical reactivity"},
        {"front": "pH Scale Range", "back": "0-14, where 7 is neutral, <7 is acidic, >7 is basic"}
    ],
    "Programming": [
        {"front": "What is a Variable?", "back": "A named container that stores a value in computer memory"},
        {"front": "Difference: var vs let vs const", "back": "var=function scoped, let=block scoped, const=immutable after assignment"},
        {"front": "Loop Types", "back": "For (fixed), While (conditional), Do-While (at least once)"},
        {"front": "Function Definition", "back": "A reusable block of code that performs a specific task"},
        {"front": "What is Recursion?", "back": "A function that calls itself with a base case to terminate"},
        {"front": "Array Index Start", "back": "Most languages: index 0 (first element is at position 0)"},
        {"front": "String Concatenation", "back": "Joining two strings together: 'Hello' + 'World' = 'HelloWorld'"},
        {"front": "True or False: Variables must be declared?", "back": "Depends on language: JavaScript (no), Java (yes), C++ (yes)"}
    ],
    "English": [
        {"front": "What is a Noun?", "back": "A word that names a person, place, thing, or idea"},
        {"front": "What is a Verb?", "back": "A word that expresses an action or a state of being"},
        {"front": "Adjective Definition", "back": "A word that describes or modifies a noun"},
        {"front": "What is an Adverb?", "back": "A word that modifies a verb, adjective, or other adverb, often ending in -ly"},
        {"front": "Subject-Verb Agreement", "back": "The subject and verb must agree in number: 'He runs' (singular), 'They run' (plural)"},
        {"front": "Simple Sentence", "back": "Contains one independent clause with one subject and one verb"},
        {"front": "Compound Sentence", "back": "Contains two independent clauses joined by a coordinating conjunction"},
        {"front": "What is a Pronoun?", "back": "A word that replaces a noun (he, she, it, they, who, which)"}
    ],
    "Aptitude": [
        {"front": "Percentage Increase Formula", "back": "(New Value - Old Value) / Old Value × 100"},
        {"front": "Average Formula", "back": "Sum of all values / Number of values"},
        {"front": "Simple Interest", "back": "SI = (P × R × T) / 100 where P=principal, R=rate, T=time"},
        {"front": "Probability Formula", "back": "P(Event) = Favorable Outcomes / Total Possible Outcomes"},
        {"front": "Ratio", "back": "A comparison of two quantities: a:b represents a/b"},
        {"front": "Prime Number", "back": "A number greater than 1 that has only two factors: 1 and itself"},
        {"front": "Compound Interest", "back": "CI = P(1 + r/100)^t - P where interest is calculated on principal and interest"},
        {"front": "Speed Formula", "back": "Speed = Distance / Time, Distance = Speed × Time"}
    ]
}

# Revision guides focusing on important exam topics
REVISION_GUIDES = {
    "Math": {
        "importantTopics": ["Laws of Motion", "Work and Energy", "Projectile Motion", "Formulas"],
        "commonMistakes": [
            "Confusing velocity with speed",
            "Forgetting to include units in answers",
            "Not considering direction in vector quantities",
            "Misapplying formulas out of context"
        ],
        "quickTips": [
            "Always draw diagrams for motion problems",
            "Check units at every step",
            "Verify answer makes physical sense",
            "Practice with real numbers before solving symbolically"
        ]
    },
    "Science": {
        "importantTopics": ["Photosynthesis", "Cell Structure", "DNA and Genetics", "Atomic Theory"],
        "commonMistakes": [
            "Mixing up mitochondria and chloroplast functions",
            "Forgetting oxygen is released during photosynthesis",
            "Confusing prokaryotes and eukaryotes",
            "Incorrect DNA base pairing"
        ],
        "quickTips": [
            "Remember: Mitochondria = Energy, Chloroplast = Photosynthesis",
            "ATP is the universal energy currency",
            "DNA: A-T, G-C pairing",
            "Use mnemonics: KPCOFGS for taxonomy"
        ]
    },
    "Programming": {
        "importantTopics": ["Variables and Data Types", "Loops", "Functions", "Arrays and Lists"],
        "commonMistakes": [
            "Off-by-one errors in loops",
            "Forgetting to initialize variables",
            "Not returning values from functions",
            "Confusing = (assignment) with == (comparison)"
        ],
        "quickTips": [
            "Test with simple inputs first",
            "Use descriptive variable names",
            "Break complex problems into functions",
            "Debug by printing intermediate values"
        ]
    },
    "English": {
        "importantTopics": ["Parts of Speech", "Sentence Structure", "Punctuation", "Grammar"],
        "commonMistakes": [
            "Subject-verb disagreement",
            "Comma splices (joining independent clauses with commas)",
            "Confusing their/there/they're",
            "Incorrect pronoun reference"
        ],
        "quickTips": [
            "Read aloud to hear mistakes",
            "Check subject-verb agreement",
            "Use 'I' and 'me' correctly in sentences",
            "A period connects two independent clauses"
        ]
    },
    "Aptitude": {
        "importantTopics": ["Percentages", "Ratios and Proportions", "Probability", "Data Interpretation"],
        "commonMistakes": [
            "Calculating percentage increase incorrectly",
            "Forgetting to simplify ratios",
            "Misunderstanding conditional probability",
            "Misreading graph axes"
        ],
        "quickTips": [
            "Percentage = (Part/Whole) × 100",
            "Always check if answer is reasonable",
            "Practice mental math for speed",
            "Re-read questions before calculating"
        ]
    }
}


@router.get("/structured/{subject}")
async def get_structured_notes(
    subject: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get structured study notebook content for a subject with topics, explanations, and examples"""
    # First try new subject_content module
    topics = _convert_subject_to_topics(subject)
    
    if not topics:
        # Fallback to old STRUCTURED_TOPICS
        topics = STRUCTURED_TOPICS.get(subject, [])
    
    if not topics:
        raise HTTPException(status_code=404, detail=f"Content not available for {subject}")
    
    return {
        "subject": subject,
        "topics": topics,
        "count": len(topics)
    }


@router.get("/flashcards/{subject}")
async def get_structured_flashcards(
    subject: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get focused flashcards for important concepts in a subject"""
    # First try new subject_content module
    flashcards = _convert_subject_to_flashcards(subject)
    
    if not flashcards:
        # Fallback to old STRUCTURED_FLASHCARDS
        flashcards = STRUCTURED_FLASHCARDS.get(subject, [])
    
    if not flashcards:
        raise HTTPException(status_code=404, detail=f"Flashcards not available for {subject}")
    
    return {
        "subject": subject,
        "flashcards": flashcards,
        "count": len(flashcards)
    }


@router.get("/revision/{subject}")
async def get_revision_guide(
    subject: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get revision guide with important topics, common mistakes, and quick tips"""
    # First try new subject_content module
    guide = _convert_subject_to_revision(subject)
    
    if not guide.get("importantTopics"):
        # Fallback to old REVISION_GUIDES
        guide = REVISION_GUIDES.get(subject, {})
    
    if not guide:
        raise HTTPException(status_code=404, detail=f"Revision guide not available for {subject}")
    
    return {
        "subject": subject,
        "importantTopics": guide.get("importantTopics", []),
        "commonMistakes": guide.get("commonMistakes", []),
        "quickTips": guide.get("quickTips", [])
    }

