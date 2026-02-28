from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from datetime import datetime, timezone
import enum
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    teacher = "teacher"
    student = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    has_taken_diagnostic = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
