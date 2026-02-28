from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    concept = Column(String, index=True)
    difficulty = Column(Integer)
    question_text = Column(Text)  # Removed unique constraint to allow similar questions
    correct_answer = Column(String)
    options = Column(Text, default="")  # Pipe-separated options
    question_type = Column(String, default="single")  # "single" or "multiple"
    is_multiple = Column(String, default="false")  # "true" or "false"