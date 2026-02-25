from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class ClassroomStudent(Base):
    __tablename__ = "classroom_students"

    id = Column(Integer, primary_key=True, index=True)

    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)