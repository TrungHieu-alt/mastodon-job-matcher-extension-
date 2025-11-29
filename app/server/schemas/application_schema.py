from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class ApplicationRequest(BaseModel):
    job_id: int
    cv_id: int


class ApplicationUpdateRequest(BaseModel):
    status: Literal["pending", "viewed", "interviewing", "rejected", "hired"]


class ApplicationResponse(BaseModel):
    app_id: int
    job_id: int
    candidate_id: int
    cv_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True