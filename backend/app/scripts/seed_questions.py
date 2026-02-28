import sys
import json
import time
import random
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.db.session import SessionLocal
from app.models.question import Question
from app.models.user import User, RoleEnum
from app.models.mastery import Mastery
from app.core.hashing import hash_password
from app.services.ai_generation.question_generator import QuestionGenerator
from app.services.ai_generation.exceptions import SchemaValidationError

TOPICS = [
    "Probability Basics",
    "Conditional Probability",
    "Bayes Theorem",
    "Random Variables",
    "Distributions",
    "Expectation and Variance"
]

QUESTIONS_PER_TOPIC = 100

# Concepts for mastery tracking
CONCEPTS = [
    "Binomial",
    "Poisson",
    "Normal",
    "Bayes",
    "Conditional"
]

# Difficulty mapping
DIFFICULTY_MAP = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}


def seed_demo_users(db):
    """Create demo users for testing"""
    
    # Check if demo users already exist
    existing_student = db.query(User).filter(User.email == "student@demo.com").first()
    existing_teacher = db.query(User).filter(User.email == "teacher@demo.com").first()
    
    if existing_student and existing_teacher:
        print("✓ Demo users already exist, skipping...")
        return
    
    # Create demo student
    demo_student = User(
        email="student@demo.com",
        password_hash=hash_password("demo123"),
        role=RoleEnum.student,
        full_name="Demo Student",
        is_active=True,
        has_taken_diagnostic=False
    )
    
    db.add(demo_student)
    db.flush()
    student_id = demo_student.id
    
    # Create demo teacher
    demo_teacher = User(
        email="teacher@demo.com",
        password_hash=hash_password("demo123"),
        role=RoleEnum.teacher,
        full_name="Demo Teacher",
        is_active=True,
        has_taken_diagnostic=False
    )
    
    db.add(demo_teacher)
    db.flush()
    
    # Initialize mastery for demo student
    for concept in CONCEPTS:
        mastery = Mastery(
            user_id=student_id,
            concept=concept,
            mastery_value=0.5,
            confidence=0.5
        )
        db.add(mastery)
    
    db.commit()
    print("✓ Demo users created successfully")
    print(f"  - student@demo.com / demo123")
    print(f"  - teacher@demo.com / demo123")


def generate_questions_for_topic(generator, topic, total_needed, db):
    """
    Generate questions for a topic using LLM.
    Returns the number of questions successfully added to DB.
    """
    questions_added = 0
    questions_skipped = 0
    attempts = 0
    batch_size = 25  # Generate in batches to avoid overwhelming the LLM
    
    while questions_added < total_needed and attempts < 5:
        try:
            remaining = total_needed - questions_added
            batch = min(batch_size, remaining)
            
            print(f"  Attempt {attempts + 1}: Generating batch of {batch} questions...")
            
            # Use the generator to create questions
            q_list = generator.generate_quiz(
                weak_topics=[],
                total_questions=batch,
                difficulty=2  # Medium difficulty
            )
            
            if not q_list:
                print(f"    ⚠ No questions generated in this batch")
                attempts += 1
                time.sleep(2)
                continue
            
            # Process each generated question
            for q_data in q_list:
                try:
                    # Extract options and correct answers
                    options_list = []
                    correct_options = []
                    
                    if "options" in q_data and q_data["options"]:
                        for opt in q_data["options"]:
                            options_list.append(opt.get("text", "").strip())
                            if opt.get("is_correct", False):
                                correct_options.append(opt.get("id", ""))
                    
                    # Skip if no options or correct answers
                    if not options_list or not correct_options:
                        questions_skipped += 1
                        continue
                    
                    # Determine question type
                    is_multiple = q_data.get("multiple_selectable", False) or q_data.get("question_type") == "multiple"
                    
                    # Store options as pipe-separated string
                    options_str = "||".join(options_list)
                    correct_str = "|".join(correct_options)
                    
                    # Map difficulty from string to integer
                    difficulty_str = q_data.get("difficulty", "medium").lower()
                    difficulty = DIFFICULTY_MAP.get(difficulty_str, 2)
                    
                    # Get concept from tags or use topic
                    concept = topic  # Default to topic
                    if q_data.get("concept_tags") and isinstance(q_data["concept_tags"], list):
                        if len(q_data["concept_tags"]) > 0:
                            concept = q_data["concept_tags"][0]
                    
                    question = Question(
                        topic=topic,
                        concept=concept,
                        difficulty=difficulty,
                        question_text=q_data.get("question_text", "").strip(),
                        correct_answer=correct_str,
                        options=options_str,
                        question_type="multiple" if is_multiple else "single",
                        is_multiple="true" if is_multiple else "false"
                    )
                    
                    db.add(question)
                    questions_added += 1
                    
                except Exception as e:
                    questions_skipped += 1
                    continue
            
            # Commit the batch
            try:
                db.commit()
                print(f"    ✓ Added {questions_added}/{total_needed} questions")
            except Exception as e:
                db.rollback()
                print(f"    ✗ Database commit failed: {str(e)}")
                questions_added -= len(q_list)  # Rollback count
            
            attempts += 1
            
        except SchemaValidationError as e:
            print(f"    ✗ Schema validation error: {str(e)}")
            attempts += 1
            time.sleep(2)
            continue
        except Exception as e:
            print(f"    ✗ Generation error: {str(e)}")
            attempts += 1
            time.sleep(2)
            continue
    
    return questions_added


def seed():
    db = SessionLocal()

    try:
        print("\n" + "="*70)
        print("DATABASE SEEDING - GENERATING QUESTIONS WITH LLM")
        print("="*70 + "\n")
        
        # Seed demo users first
        seed_demo_users(db)
        
        # Check if questions already exist and ask to clear
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"\n⚠ Found {existing_count} existing questions in database")
            response = input("Clear existing questions and regenerate? (yes/no): ").strip().lower()
            if response == "yes":
                print("Clearing existing questions...")
                db.query(Question).delete()
                db.commit()
                print("✓ Questions cleared\n")
            else:
                print("✓ Skipping generation, using existing questions\n")
                db.close()
                return
        
        # Initialize LLM generator
        print("Initializing LLM question generator...")
        try:
            generator = QuestionGenerator()
            print("✓ LLM generator initialized\n")
        except Exception as e:
            print(f"✗ Failed to initialize generator: {str(e)}")
            print("Make sure HF_API_KEY is set in .env file")
            db.close()
            return
        
        # Generate questions for each topic
        total_generated = 0
        
        for topic in TOPICS:
            print(f"\n📚 Topic: {topic}")
            print(f"  Target: {QUESTIONS_PER_TOPIC} questions\n")
            
            try:
                added = generate_questions_for_topic(
                    generator,
                    topic,
                    QUESTIONS_PER_TOPIC,
                    db
                )
                total_generated += added
                
                print(f"  ✓ Successfully added {added} questions for {topic}\n")
                
                # Small delay between topics to avoid overwhelming the API
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error generating questions for {topic}: {str(e)}\n")
                db.rollback()
                continue
        
        # Final verification
        final_count = db.query(Question).count()
        print("\n" + "="*70)
        print(f"✓ SEEDING COMPLETE!")
        print(f"  Total questions in database: {final_count}")
        print(f"  Target was: {len(TOPICS) * QUESTIONS_PER_TOPIC}")
        print("="*70 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n✗ Fatal error during seeding: {e}\n")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    seed()