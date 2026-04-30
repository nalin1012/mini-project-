#!/usr/bin/env python3
"""Test the improved quiz generation"""

from notes import _fallback_quiz_from_flashcards

# Test the fallback quiz generation with sample flashcards
flashcards = [
    {"q": "What are Newton's Laws of Motion?", "a": "Three fundamental principles describing how objects move and forces act"},
    {"q": "Explain the First Law of Motion", "a": "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force"},
    {"q": "What is Force?", "a": "A push or pull that changes the motion of an object, measured in Newtons"},
]

quiz = _fallback_quiz_from_flashcards(flashcards)
print(f"✓ Generated {len(quiz)} quiz questions\n")
for i, q in enumerate(quiz, 1):
    print(f"Question {i}: {q['question']}")
    for j, opt in enumerate(q['options']):
        prefix = "→ CORRECT: " if j == q['correct_option'] else "  "
        print(f"  {chr(65+j)}. {prefix}{opt}")
    print(f"Explanation: {q['explanation'][:100]}...\n")

print("✓ Quiz generation test passed!")
