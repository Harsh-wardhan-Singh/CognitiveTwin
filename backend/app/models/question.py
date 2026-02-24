from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    concept_tag = Column(String, index=True)
    question_text = Column(String, nullable=False)

    metadata_json = Column(JSON, nullable=True)