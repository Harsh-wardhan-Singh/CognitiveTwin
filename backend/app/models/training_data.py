from sqlalchemy import Column, Integer, JSON
from app.db.base import Base

class TrainingData(Base):
    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, index=True)
    features = Column(JSON, nullable=False)
    label = Column(Integer, nullable=False)