from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    concept = Column(String, index=True)
    difficulty = Column(Integer)
    question_text = Column(Text, unique=True)
    correct_answer = Column(String)