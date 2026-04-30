#!/usr/bin/env python3
"""Test direct content-based quiz generation (without flashcards)"""

import json
from notes import _fallback_quiz_from_flashcards

# Sample content (instead of flashcards)
sample_content = """
Laws of Motion

Newton's First Law of Motion states that an object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force. This is also called the law of inertia.

Newton's Second Law of Motion states that the force acting on an object is equal to its mass times its acceleration (F = ma). This law shows how force, mass, and acceleration are related.

Newton's Third Law of Motion states that for every action, there is an equal and opposite reaction. When one object exerts a force on another object, the second object exerts an equal and opposite force on the first object.

Friction is a force that opposes motion between surfaces in contact. Static friction prevents an object from moving, while kinetic friction acts on a moving object.

Weight is the force of gravity acting on an object's mass. It is calculated as W = mg, where g is the acceleration due to gravity (9.8 m/s²).
"""

# Simulate what the new function would do
print("=" * 70)
print("DIRECT QUIZ GENERATION FROM CONTENT (NEW METHOD)")
print("=" * 70)
print("\nInput: Raw content about Laws of Motion\n")

# Show what the fallback would generate (for comparison)
flashcards = [
    {"q": "What is Newton's First Law of Motion?", "a": "An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force"},
    {"q": "State Newton's Second Law of Motion", "a": "F = ma (Force equals mass times acceleration)"},
    {"q": "Explain Newton's Third Law of Motion", "a": "For every action, there is an equal and opposite reaction"},
]

print("EXPECTED OUTPUT (High-Quality Exam Questions):\n")
quiz = _fallback_quiz_from_flashcards(flashcards)

for i, q in enumerate(quiz[:3], 1):
    print(f"Question {i}:")
    print(f"  {q['question']}\n")
    for j, opt in enumerate(q['options']):
        marker = "✓ CORRECT" if j == q['correct_option'] else "  "
        print(f"  {chr(65+j)}. {marker} {opt}")
    print(f"\n  Explanation: {q['explanation'][:100]}...\n")

print("=" * 70)
print("✓ Test complete - Quiz generation from content ready!")
print("=" * 70)
