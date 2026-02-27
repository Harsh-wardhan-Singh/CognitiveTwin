from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MasteryCreate(BaseModel):
    concept: str
    mastery_value: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class MasteryUpdate(BaseModel):
    mastery_value: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class MasteryResponse(BaseModel):
    id: int
    user_id: int
    concept: str
    mastery_value: float
    confidence: float

    class Config:
        from_attributes = True


class MasterySnapshot(BaseModel):
    """Current mastery state for a student across all concepts"""
    user_id: int
    mastery: dict  # concept -> mastery_value


class DashboardMasteryData(BaseModel):
    """Dashboard view of mastery data"""
    concepts: List[str]
    values: List[float]
    confidences: List[float]
    trends: Optional[dict] = None
