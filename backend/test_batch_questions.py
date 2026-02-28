"""
Test script to generate a full batch of questions to diagnose JSON issues
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.ai_generation.question_generator import QuestionGenerator

print("Testing full batch question generation (25 questions)...\n")

try:
    gen = QuestionGenerator()
    
    questions = gen.generate_quiz(
        weak_topics=[],
        total_questions=25,
        difficulty=2
    )
    
    print(f"✓ Successfully generated {len(questions)} questions!")
    
    if questions:
        print(f"\nFirst question:")
        q = questions[0]
        print(f"  ID: {q.get('question_id')}")
        print(f"  Text: {q.get('question_text', 'N/A')[:60]}...")
        print(f"  Options: {len(q.get('options', []))} options")
        print(f"  Correct: {[o['id'] for o in q.get('options', []) if o.get('is_correct')]}")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
