from base import Base
from session import engine

# Import ALL models so SQLAlchemy registers them
from app.models import user, question, attempt, mastery, classroom,mastery_history

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()