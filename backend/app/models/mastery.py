from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db.base import Base

class Mastery(Base):
    __tablename__ = "mastery"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    concept = Column(String, index=True)
    mastery_value = Column(Float)
    confidence = Column(Float)