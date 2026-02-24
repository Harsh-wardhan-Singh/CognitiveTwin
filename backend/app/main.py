from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.classroom import Classroom
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.mastery import Mastery

app = FastAPI(
    title="Cognitive Twin Backend",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend running"}