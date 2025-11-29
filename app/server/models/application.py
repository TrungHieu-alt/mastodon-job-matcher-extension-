# models/application.py
from beanie import Document
from datetime import datetime
from typing import Literal


class Application(Document):
    id: int
    job_id: int
    candidate_id: int
    cv_id: int
    status: Literal["pending", "viewed", "interviewing", "rejected", "hired"] = "pending"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "applications"
