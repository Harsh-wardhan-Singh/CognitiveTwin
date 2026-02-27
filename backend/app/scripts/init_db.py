"""
Database initialization script
Creates sample data for testing
"""

import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User, RoleEnum
from app.models.question import Question
from app.models.classroom import Classroom
from app.models.mastery import Mastery
from app.core.hashing import hash_password


def init_db():
    """Initialize database with sample data"""
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data (for testing)
        # Uncomment the following lines if you want a fresh start
        # db.query(Mastery).delete()
        # db.query(Question).delete()
        # db.query(Classroom).delete()
        # db.query(User).delete()
        # db.commit()
        
        # Create sample users
        print("Creating sample users...")
        
        # Teacher
        teacher = User(
            email="teacher@example.com",
            password_hash=hash_password("password123"),
            role=RoleEnum.teacher,
            full_name="Ms. Analytics"
        )
        db.add(teacher)
        db.flush()
        
        # Students
        students = []
        for i in range(5):
            student = User(
                email=f"student{i+1}@example.com",
                password_hash=hash_password("password123"),
                role=RoleEnum.student,
                full_name=f"Student {i+1}"
            )
            db.add(student)
            students.append(student)
        
        db.flush()
        
        # Create sample classroom
        print("Creating sample classroom...")
        classroom = Classroom(
            name="Probability 101",
            subject="Statistics",
            teacher_id=teacher.id,
            syllabus_scope=["Binomial", "Poisson", "Normal"],
            exam_pattern="MCQ + Short Answer",
            progress_topics=["Binomial", "Poisson"]
        )
        db.add(classroom)
        db.flush()
        
        # Create sample questions
        print("Creating sample questions...")
        questions = [
            Question(
                topic="Binomial",
                concept="Binomial Distribution",
                difficulty=2,
                question_text="What is E[X] for Binomial(n,p)?",
                correct_answer="n × p"
            ),
            Question(
                topic="Binomial",
                concept="Binomial Distribution",
                difficulty=3,
                question_text="What is Var(X) for Binomial(n,p)?",
                correct_answer="n × p × (1-p)"
            ),
            Question(
                topic="Poisson",
                concept="Poisson Distribution",
                difficulty=2,
                question_text="Variance of Poisson(λ) is?",
                correct_answer="λ"
            ),
            Question(
                topic="Poisson",
                concept="Poisson Distribution",
                difficulty=3,
                question_text="Poisson distribution is used for?",
                correct_answer="rare events"
            ),
            Question(
                topic="Normal",
                concept="Normal Distribution",
                difficulty=2,
                question_text="Mean of Normal(μ, σ²) is?",
                correct_answer="μ"
            ),
            Question(
                topic="Normal",
                concept="Normal Distribution",
                difficulty=3,
                question_text="Approximately what percentage of data falls within 2σ of the mean?",
                correct_answer="95"
            ),
        ]
        
        for q in questions:
            db.add(q)
        
        db.flush()
        
        # Initialize masteries for students
        print("Creating sample mastery data...")
        for student in students:
            for concept in ["Binomial Distribution", "Poisson Distribution", "Normal Distribution"]:
                mastery = Mastery(
                    user_id=student.id,
                    concept=concept,
                    mastery_value=0.5,  # Cold start
                    confidence=0.5
                )
                db.add(mastery)
        
        db.commit()
        print("✅ Database initialized successfully!")
        print(f"   - Created {len(students)} students")
        print(f"   - Created 1 teacher")
        print(f"   - Created 1 classroom")
        print(f"   - Created {len(questions)} sample questions")
        print(f"   - Initialized mastery for {len(students)} students")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
