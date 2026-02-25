from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_services import register_user, login_user
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data.email, data.password, data.role)


@router.post("/login")
def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):

    token = login_user(db, data.email, data.password)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,      # True in production (HTTPS)
        samesite="lax"
    )

    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",   # must match how you set it in login
        secure=False      # change to True in production (HTTPS)
    )
    return {"message": "Logged out successfully"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }