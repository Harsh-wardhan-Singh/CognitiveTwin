from fastapi import FastAPI , Depends
from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.classroom import Classroom
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.mastery import Mastery
from app.core.dependencies import get_current_user
from app.api.auth_routes import router as auth_router

app = FastAPI(
    title="Cognitive Twin Backend",
    version="1.0.0"
)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"user": user}

from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models.user import User

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend running"}