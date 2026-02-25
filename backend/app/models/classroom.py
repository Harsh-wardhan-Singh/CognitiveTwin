from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)