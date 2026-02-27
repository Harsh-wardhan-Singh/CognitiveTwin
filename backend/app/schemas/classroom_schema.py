from pydantic import BaseModel
from typing import Optional, List, Any


class ClassroomCreate(BaseModel):
    name: str
    subject: Optional[str] = None
    syllabus_scope: Optional[str] = None
    exam_pattern: Optional[str] = None
    progress_topics: Optional[List[str]] = None


class ClassroomResponse(BaseModel):
    id: int
    name: str
    subject: Optional[str] = None

    class Config:
        from_attributes = True