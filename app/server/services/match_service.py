from typing import Optional, List
from repositories.match_repo import MatchRepository
from models.matchResult import MatchResult


class MatchService:
    @staticmethod
    async def get_cv_matches(cv_id: int) -> List[MatchResult]:
        return await MatchRepository.get_by_cv_id(cv_id)

    @staticmethod
    async def get_job_matches(job_id: int) -> List[MatchResult]:
        return await MatchRepository.get_by_job_id(job_id)

    @staticmethod
    async def recompute_cv_match(cv_id: int) -> List[MatchResult]:
        # Stub: Placeholder for actual matching algorithm
        return await MatchRepository.get_by_cv_id(cv_id)

    @staticmethod
    async def recompute_job_match(job_id: int) -> List[MatchResult]:
        # Stub: Placeholder for actual matching algorithm
        return await MatchRepository.get_by_job_id(job_id)