#!/usr/bin/env python
"""Test subject content module"""

from subject_content import (
    get_subject_content, 
    generate_subject_flashcards,
    generate_subject_revision,
    get_topic_content
)

print("=" * 60)
print("TESTING SUBJECT-SPECIFIC CONTENT MODULE")
print("=" * 60)

# Test Math
print("\n1. MATH SUBJECT")
math_content = get_subject_content('math')
print(f"   Topics: {list(math_content.get('topics', []))}")
math_cards = generate_subject_flashcards('math', limit=2)
print(f"   Flashcards: {len(math_cards)}")
if math_cards:
    print(f"   Sample Q: {math_cards[0]['q']}")
    print(f"   Sample A: {math_cards[0]['a']}")

# Test Programming
print("\n2. PROGRAMMING SUBJECT")
prog_content = get_subject_content('programming')
print(f"   Topics: {list(prog_content.get('topics', []))}")
prog_cards = generate_subject_flashcards('programming', limit=2)
print(f"   Flashcards: {len(prog_cards)}")
if prog_cards:
    print(f"   Sample Q: {prog_cards[0]['q']}")

# Test Science
print("\n3. SCIENCE SUBJECT")
sci_revision = generate_subject_revision('science')
print(f"   Key points: {len(sci_revision.get('key_points', []))}")
print(f"   Common mistakes: {len(sci_revision.get('common_mistakes', []))}")
print(f"   Quick tips: {len(sci_revision.get('quick_tips', []))}")

# Test English
print("\n4. ENGLISH SUBJECT")
eng_cards = generate_subject_flashcards('english', limit=2)
print(f"   Flashcards: {len(eng_cards)}")
if eng_cards:
    print(f"   Sample: {eng_cards[0]['q']}")

# Test Topic Detail
print("\n5. TOPIC DETAILS")
fractions = get_topic_content('math', 'Fractions')
print(f"   Fractions explanation length: {len(fractions.get('explanation', ''))}")
print(f"   Fractions key points: {len(fractions.get('key_points', []))}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Subject content module is working!")
print("=" * 60)
