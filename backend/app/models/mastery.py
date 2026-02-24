from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime , timezone
from app.db.base import Base


class Mastery(Base):
    __tablename__ = "mastery"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, nullable=False)
    concept_tag = Column(String, nullable=False)

    mastery_score = Column(Float, default=0.0)

    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))