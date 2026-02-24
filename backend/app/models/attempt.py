from sqlalchemy import Column, Integer, ForeignKey, Boolean, Float, DateTime
from datetime import datetime , timezone
from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    correct = Column(Boolean, default=False)
    confidence = Column(Integer)
    time_taken = Column(Float)
    reclick_count = Column(Integer)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))