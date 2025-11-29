from beanie import Document
from datetime import datetime
from pymongo import IndexModel


class MatchResult(Document):
    id: int
    cv_id: int
    job_id: int
    score: float
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "match_results"
        indexes = [
            IndexModel([("cv_id", 1), ("job_id", 1)], unique=True)
        ]
