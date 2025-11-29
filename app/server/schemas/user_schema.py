from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["candidate", "recruiter"]


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    email: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"