# models/user.py
from beanie import Document
from datetime import datetime
from typing import Literal


class User(Document):
    user_id: int
    email: str
    password_hash: str
    role: Literal["candidate", "recruiter"]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"
