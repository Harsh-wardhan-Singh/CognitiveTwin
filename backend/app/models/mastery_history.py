from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class MasteryHistory(Base):
    __tablename__ = "mastery_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    concept = Column(String, index=True)

    mastery_value = Column(Float)
    confidence = Column(Float)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())