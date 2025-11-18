from beanie import Document
from typing import List, Optional

class Candidate(Document):
    user_id: str
    title: str
    skills: List[str] = []
    summary: Optional[str]
    experience: Optional[str]
    location: Optional[str]
    availability: Optional[str]

    class Settings:
        name = "candidates"
