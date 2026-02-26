from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, JSON
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    syllabus_scope = Column(JSON, nullable=True)
    exam_pattern = Column(JSON, nullable=True)
    progress_topics = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    teacher = relationship("User", backref="classrooms")
