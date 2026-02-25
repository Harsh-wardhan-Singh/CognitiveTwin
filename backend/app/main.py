from fastapi import FastAPI, Depends
from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.classroom import Classroom
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.mastery import Mastery
from app.models.classroom_student import ClassroomStudent

from app.core.dependencies import get_current_user
from app.api.auth_routes import router as auth_router
from app.api.teacher_routes import router as teacher_router
from app.api.student_routes import router as student_router

app = FastAPI(
    title="Cognitive Twin Backend",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(student_router)

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"user": user.email}