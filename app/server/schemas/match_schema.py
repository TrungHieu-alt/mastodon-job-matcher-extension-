from pydantic import BaseModel
from datetime import datetime


class MatchResultResponse(BaseModel):
    cv_id: int
    job_id: int
    score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True