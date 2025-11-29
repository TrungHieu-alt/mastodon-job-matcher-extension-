from typing import Optional, List
from models.matchResult import MatchResult


class MatchRepository:
    @staticmethod
    async def create_or_update(cv_id: int, job_id: int, score: float) -> MatchResult:
        existing = await MatchResult.find_one(
            (MatchResult.cv_id == cv_id) & (MatchResult.job_id == job_id)
        )
        if existing:
            await existing.update({"$set": {"score": score}})
            return await MatchRepository.get_by_cv_job(cv_id, job_id)
        
        match = MatchResult(cv_id=cv_id, job_id=job_id, score=score)
        await match.insert()
        return match

    @staticmethod
    async def get_by_cv_job(cv_id: int, job_id: int) -> Optional[MatchResult]:
        return await MatchResult.find_one(
            (MatchResult.cv_id == cv_id) & (MatchResult.job_id == job_id)
        )

    @staticmethod
    async def get_by_cv_id(cv_id: int) -> List[MatchResult]:
        return await MatchResult.find(MatchResult.cv_id == cv_id).to_list(None)

    @staticmethod
    async def get_by_job_id(job_id: int) -> List[MatchResult]:
        return await MatchResult.find(MatchResult.job_id == job_id).to_list(None)