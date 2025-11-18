from beanie import Document
from typing import Optional, Dict

class CVDocument(Document):
    candidate_id: str
    template: str
    data: Dict
    thumbnail: Optional[str]

    class Settings:
        name = "cv_documents"
