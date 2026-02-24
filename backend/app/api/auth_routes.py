from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_services import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data.email, data.password, data.role)


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)