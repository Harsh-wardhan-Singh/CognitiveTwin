"""
Diagnostic script to test LLM connectivity and API key validity
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*70)
print("LLM API DIAGNOSTIC TEST")
print("="*70 + "\n")

# Step 1: Check if .env is loaded
hf_key = os.getenv("HF_API_KEY")
db_url = os.getenv("DATABASE_URL")

print("1. Environment Variables:")
if hf_key:
    print(f"   ✓ HF_API_KEY found (length: {len(hf_key)} chars)")
    print(f"     First 10 chars: {hf_key[:10]}...")
else:
    print(f"   ✗ HF_API_KEY not found")
    sys.exit(1)

if db_url:
    print(f"   ✓ DATABASE_URL found")
else:
    print(f"   ✗ DATABASE_URL not found")

print("\n2. Testing LLM Client Initialization:")
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.services.ai_generation.llm_client import LLMClient
    
    client = LLMClient()
    print("   ✓ LLMClient initialized successfully")
except Exception as e:
    print(f"   ✗ Failed to initialize LLMClient: {str(e)}")
    sys.exit(1)

print("\n3. Testing Simple API Call:")
try:
    response = client.generate_json(
        system_prompt="You are a helpful assistant.",
        user_prompt='Return {"test": "success"} and nothing else.'
    )
    print(f"   ✓ API call successful!")
    print(f"   Response preview: {response[:100]}...")
except Exception as e:
    print(f"   ✗ API call failed: {str(e)}")
    sys.exit(1)

print("\n4. Testing Question Generation:")  
try:
    from app.services.ai_generation.question_generator import QuestionGenerator
    
    gen = QuestionGenerator()
    print("   ✓ QuestionGenerator initialized")
    
    # Try generating a small batch
    questions = gen.generate_quiz(
        weak_topics=[],
        total_questions=5,
        difficulty=2
    )
    print(f"   ✓ Generated {len(questions)} questions")
    
    if questions:
        q = questions[0]
        print(f"   Sample question: {q.get('question_text', 'N/A')[:50]}...")
        
except Exception as e:
    print(f"   ✗ Question generation failed: {str(e)}")
    sys.exit(1)

print("\n" + "="*70)
print("✓ ALL TESTS PASSED - Ready to seed database!")
print("="*70 + "\n")
