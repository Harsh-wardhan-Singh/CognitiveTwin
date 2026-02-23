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