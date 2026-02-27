from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AttemptCreate(BaseModel):
    question_id: int
    is_correct: bool
    confidence: int = Field(..., ge=1, le=10)
    response_time: Optional[float] = None


class AttemptResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    is_correct: bool
    confidence: int

    class Config:
        from_attributes = True
