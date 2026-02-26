from pydantic import BaseModel
from typing import Optional, Dict


class ClassroomCreate(BaseModel):
    name: str
    subject: str
    syllabus_scope: Optional[Dict] = None
    exam_pattern: Optional[Dict] = None
    progress_topics: Optional[Dict] = None


class ClassroomResponse(BaseModel):
    id: int
    name: str
    subject: str

    class Config:
        from_attributes = True