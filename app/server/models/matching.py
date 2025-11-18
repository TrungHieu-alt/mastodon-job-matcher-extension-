from beanie import Document
from datetime import datetime
from typing import Optional

class Matching(Document):
    job_id: str
    candidate_id: str
    score: Optional[int] = None  
    status: Optional[str] = None  
    updated_at: datetime = datetime.now(datetime.timezone.utc)

    class Settings:
        name = "matching"
    