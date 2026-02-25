import random
from app.db.session import SessionLocal
from app.models.question import Question
from app.services.ai_generation.question_generator import generate_question

TOPICS = [
    "Probability Basics",
    "Conditional Probability",
    "Bayes Theorem",
    "Random Variables",
    "Distributions",
    "Expectation and Variance"
]

QUESTIONS_PER_TOPIC = 100


def seed():
    db = SessionLocal()

    try:
        for topic in TOPICS:
            print(f"Generating questions for {topic}...")

            for i in range(QUESTIONS_PER_TOPIC):
                q_data = generate_question(topic)

                if not validate_question(q_data):
                    print("Invalid question skipped")
                    continue

                question = Question(
                    topic=topic,
                    concept=q_data["concept"],
                    difficulty=q_data["difficulty"],
                    question_text=q_data["question"],
                    correct_answer=q_data["correct_answer"]
                )

                db.add(question)

            db.commit()

        print("Seeding complete.")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


def validate_question(q_data):
    required_keys = ["concept", "difficulty", "question", "correct_answer"]
    return all(k in q_data for k in required_keys)


if __name__ == "__main__":
    seed()