from beanie import Document
from typing import List, Optional

class Job(Document):
    recruiter_id: str
    title: str
    company: str
    location: Optional[str]
    salary: Optional[str]
    description: Optional[str]
    requirements: List[str] = []
    logo: Optional[str]
    status: str = "open"

    class Settings:
        name = "jobs"
