"""
Quiz model for teacher-created tests
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from datetime import datetime
from app.db.base import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    topic = Column(String, index=True)
    difficulty = Column(String)  # easy, medium, hard
    num_questions = Column(Integer)
    
    # Store question IDs for this quiz
    question_ids = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
