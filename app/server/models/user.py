from beanie import Document
from typing import Optional
from pydantic import EmailStr

class User(Document):
    email: EmailStr
    password_hash: str
    role: str  # candidate | recruiter | admin
    name: str
    avatar: Optional[str] = None
    location: Optional[str] = None

    class Settings:
        name = "users"
