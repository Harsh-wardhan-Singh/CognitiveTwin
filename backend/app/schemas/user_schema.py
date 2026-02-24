from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum


class UserLogin(BaseModel):
    email: EmailStr
    password: str