import random
from app.db.session import SessionLocal
from app.models.question import Question
from app.models.user import User, RoleEnum
from app.models.mastery import Mastery
from app.core.hashing import hash_password
from app.services.ai_generation.question_generator import QuestionGenerator

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
        is_active=True
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
        is_active=True
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


def seed():
    db = SessionLocal()

    try:
        print("\n" + "="*60)
        print("DATABASE SEEDING")
        print("="*60 + "\n")
        
        # Seed demo users first
        seed_demo_users(db)
        
        # Check if questions already exist
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"✓ Questions already exist ({existing_count}), skipping generation...\n")
            db.close()
            return
        
        generator = QuestionGenerator()
        total_generated = 0
        
        for topic in TOPICS:
            print(f"Generating {QUESTIONS_PER_TOPIC} questions for {topic}...")
            
            try:
                # Generate questions for this topic
                q_list = generator.generate_quiz(
                    weak_topics=[],
                    total_questions=QUESTIONS_PER_TOPIC,
                    difficulty=2  # Medium difficulty
                )
                
                for q_data in q_list:
                    if not validate_question(q_data):
                        continue
                    
                    # Extract options and correct answers
                    options_list = []
                    correct_options = []
                    
                    if "options" in q_data and q_data["options"]:
                        for opt in q_data["options"]:
                            options_list.append(opt.get("text", ""))
                            if opt.get("is_correct", False):
                                correct_options.append(opt.get("id", ""))
                    
                    # Determine question type
                    question_type = q_data.get("question_type", "single")
                    is_multiple = question_type == "multiple" or q_data.get("multiple_selectable", False)
                    
                    # Store options as pipe-separated string
                    options_str = "||".join(options_list) if options_list else ""
                    correct_str = "|".join(correct_options) if correct_options else ""
                    
                    question = Question(
                        topic=topic,
                        concept=q_data.get("concept_tags", [topic])[0] if q_data.get("concept_tags") else topic,
                        difficulty=q_data.get("difficulty", 2) if isinstance(q_data.get("difficulty"), int) else 2,
                        question_text=q_data.get("question_text", ""),
                        correct_answer=correct_str,
                        options=options_str,
                        question_type=question_type,
                        is_multiple="true" if is_multiple else "false"
                    )
                    
                    db.add(question)
                    total_generated += 1
                
                db.commit()
                print(f"  ✓ Added {len(q_list)} questions\n")
                
            except Exception as e:
                print(f"  ✗ Error generating questions: {str(e)}\n")
                db.rollback()
                continue
        
        print(f"✓ Seeding complete! Total questions generated: {total_generated}\n")

    except Exception as e:
        db.rollback()
        print(f"\n✗ Error during seeding: {e}\n")
        import traceback
        traceback.print_exc()

    finally:
        db.close()
        db.close()


def validate_question(q_data):
    required_keys = ["concept", "difficulty", "question", "correct_answer"]
    return all(k in q_data for k in required_keys)


if __name__ == "__main__":
    seed()