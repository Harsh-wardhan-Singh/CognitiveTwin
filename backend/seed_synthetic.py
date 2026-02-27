#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from app.db.session import SessionLocal
from app.models.question import Question
from app.models.user import User, RoleEnum
from app.models.mastery import Mastery
from app.core.hashing import hash_password

TOPICS = [
    "Probability Basics",
    "Conditional Probability",
    "Bayes Theorem",
    "Random Variables",
    "Distributions",
    "Expectation and Variance"
]

CONCEPTS = ["Binomial", "Poisson", "Normal", "Bayes", "Conditional"]

# Synthetic questions
QUESTIONS = [
    # Binomial
    {
        "topic": "Probability Basics",
        "concept": "Binomial",
        "difficulty": 2,
        "question": "What is E[X] for Binomial(n,p)?",
        "options": ["n + p", "n × p", "p / n", "n²p"],
        "correct": ["n × p"],
        "multi": False
    },
    {
        "topic": "Probability Basics",
        "concept": "Binomial",
        "difficulty": 3,
        "question": "Which are properties of Binomial distribution?",
        "options": ["Fixed number of trials", "Independent trials", "Continuous outcomes", "Two outcomes per trial", "Constant p"],
        "correct": ["Fixed number of trials", "Independent trials", "Two outcomes per trial", "Constant p"],
        "multi": True
    },
    # Poisson
    {
        "topic": "Distributions",
        "concept": "Poisson",
        "difficulty": 2,
        "question": "Variance of Poisson(λ)?",
        "options": ["λ", "λ²", "√λ", "λ+1"],
        "correct": ["λ"],
        "multi": False
    },
    {
        "topic": "Distributions",
        "concept": "Poisson",
        "difficulty": 3,
        "question": "Poisson distribution models:",
        "options": ["Rare events", "Continuous outcomes", "Mean = Variance", "Requires fixed n", "Events independent"],
        "correct": ["Rare events", "Mean = Variance", "Events independent"],
        "multi": True
    },
    # Normal
    {
        "topic": "Distributions",
        "concept": "Normal",
        "difficulty": 2,
        "question": "Mean of Normal(μ, σ²)?",
        "options": ["μ", "σ", "μ²", "σ²"],
        "correct": ["μ"],
        "multi": False
    },
    {
        "topic": "Distributions",
        "concept": "Normal",
        "difficulty": 3,
        "question": "Normal distribution properties:",
        "options": ["Symmetric", "Continuous", "Defined by μ and σ²", "Bell-shaped", "Discrete"],
        "correct": ["Symmetric", "Continuous", "Defined by μ and σ²", "Bell-shaped"],
        "multi": True
    },
    # Bayes
    {
        "topic": "Bayes Theorem",
        "concept": "Bayes",
        "difficulty": 2,
        "question": "Bayes' theorem updates:",
        "options": ["Likelihood", "Prior", "Posterior", "Variance"],
        "correct": ["Posterior"],
        "multi": False
    },
    {
        "topic": "Bayes Theorem",
        "concept": "Bayes",
        "difficulty": 3,
        "question": "Components of Bayes' Theorem:",
        "options": ["Prior", "Likelihood", "Posterior", "Marginal", "Variance"],
        "correct": ["Prior", "Likelihood", "Posterior", "Marginal"],
        "multi": True
    },
    # Conditional
    {
        "topic": "Conditional Probability",
        "concept": "Conditional",
        "difficulty": 2,
        "question": "P(A|B) means:",
        "options": ["P(A)", "P(B)", "P(A given B)", "P(A and B)"],
        "correct": ["P(A given B)"],
        "multi": False
    },
    {
        "topic": "Conditional Probability",
        "concept": "Conditional",
        "difficulty": 3,
        "question": "Conditional probability rules:",
        "options": ["P(A|B)=P(A∩B)/P(B)", "Requires P(B)≠0", "Equals P(A)", "Depends on B", "Symmetric"],
        "correct": ["P(A|B)=P(A∩B)/P(B)", "Requires P(B)≠0", "Depends on B"],
        "multi": True
    }
]

def seed_demo_users(db):
    """Create demo users"""
    # Check if exist
    student = db.query(User).filter(User.email == "student@demo.com").first()
    teacher = db.query(User).filter(User.email == "teacher@demo.com").first()
    
    if student and teacher:
        print("✓ Demo users already exist")
        return
    
    if not student:
        student = User(
            email="student@demo.com",
            password_hash=hash_password("demo123"),
            role=RoleEnum.student,
            full_name="Demo Student",
            is_active=True
        )
        db.add(student)
        db.flush()
        
        # Initialize mastery
        for concept in CONCEPTS:
            mastery = Mastery(
                user_id=student.id,
                concept=concept,
                mastery_value=0.5,
                confidence=0.5
            )
            db.add(mastery)
    
    if not teacher:
        teacher = User(
            email="teacher@demo.com",
            password_hash=hash_password("demo123"),
            role=RoleEnum.teacher,
            full_name="Demo Teacher",
            is_active=True
        )
        db.add(teacher)
    
    db.commit()
    print("✓ Demo users created")

def seed():
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("DATABASE SEEDING (SYNTHETIC)")
        print("="*60 + "\n")
        
        seed_demo_users(db)
        
        # Clear existing questions
        db.query(Question).delete()
        db.commit()
        
        # Add synthetic questions multiple times to reach ~100 per topic
        count = 0
        for topic in TOPICS:
            print(f"Seeding questions for {topic}...")
            topic_questions = [q for q in QUESTIONS if q["topic"] == topic]
            
            # If no questions exist for this topic, create placeholders
            if not topic_questions:
                print(f"  ⚠ No questions defined for {topic}, skipping...")
                continue
            
            # Repeat questions to reach ~100 per topic
            repeats = max(1, 100 // len(topic_questions))
            for i in range(repeats):
                for q_data in topic_questions:
                    options_str = "||".join(q_data["options"])
                    correct_str = "|".join(q_data["correct"])
                    
                    q = Question(
                        topic=q_data["topic"],
                        concept=q_data["concept"],
                        difficulty=q_data["difficulty"],
                        question_text=q_data["question"] + f" (v{i+1})",
                        correct_answer=correct_str,
                        options=options_str,
                        question_type="multiple" if q_data["multi"] else "single",
                        is_multiple="true" if q_data["multi"] else "false"
                    )
                    db.add(q)
                    count += 1
            
            db.commit()
            print(f"  ✓ Added ~100 questions")
        
        print(f"\n✓ Seeding complete! Total questions: {count}\n")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
