import motor.motor_asyncio
from beanie import init_beanie
from models.user import User
from models.candidate import Candidate
from models.cv import CVDocument
from models.job import Job
from models.application import JobApplication
from models.score import MatchingScore

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.jobmatcher

    await init_beanie(
        database=db,
        document_models=[User, Candidate, CVDocument, Job, JobApplication, MatchingScore]
    )
