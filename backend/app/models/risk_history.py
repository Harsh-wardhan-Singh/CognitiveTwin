from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class RiskHistory(Base):
    __tablename__ = "risk_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    risk_label = Column(Integer)
    risk_score = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())