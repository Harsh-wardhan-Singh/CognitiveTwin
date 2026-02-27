from pydantic import BaseModel, Field
from typing import List, Optional


class QuestionCreate(BaseModel):
    topic: str
    concept: str
    difficulty: int = Field(..., ge=1, le=10)
    question_text: str
    correct_answer: str


class QuestionResponse(BaseModel):
    id: int
    topic: str
    concept: str
    difficulty: int
    question_text: str
    correct_answer: str

    class Config:
        from_attributes = True


class QuestionForQuiz(BaseModel):
    """Question as presented to student in quiz (no correct answer visible)"""
    id: int
    topic: str
    concept: str
    difficulty: int
    question_text: str


class SubmitAnswerRequest(BaseModel):
    question_id: int
    user_answer: str
    confidence: int = Field(..., ge=1, le=10)
    response_time: float  # milliseconds
