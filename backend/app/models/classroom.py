from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime , timezone
from app.db.base import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    syllabus_scope = Column(JSON, nullable=True)
    exam_pattern = Column(JSON, nullable=True)
    progress_topics = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    teacher = relationship("User", backref="classrooms")