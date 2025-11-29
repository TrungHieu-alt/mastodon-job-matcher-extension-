from typing import Optional, List
from fastapi import HTTPException, status
from repositories.cv_repo import CVRepository
from models.candidateResume import CandidateResume


class CVService:
    @staticmethod
    async def create_cv(user_id: int, title: str, location: Optional[str],
                       experience_years: int, skills: list, summary: Optional[str],
                       full_text: Optional[str], pdf_url: Optional[str], is_main: bool) -> CandidateResume:
        return await CVRepository.create(user_id, title, location, experience_years, skills,
                                        summary, full_text, pdf_url, is_main)

    @staticmethod
    async def get_cv(cv_id: int) -> Optional[CandidateResume]:
        cv = await CVRepository.get_by_id(cv_id)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found",
            )
        return cv

    @staticmethod
    async def get_user_cvs(user_id: int) -> List[CandidateResume]:
        return await CVRepository.get_by_user_id(user_id)

    @staticmethod
    async def get_main_cv(user_id: int) -> Optional[CandidateResume]:
        cv = await CVRepository.get_main_by_user_id(user_id)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Main CV not found",
            )
        return cv

    @staticmethod
    async def update_cv(cv_id: int, **kwargs) -> Optional[CandidateResume]:
        cv = await CVRepository.update(cv_id, **kwargs)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found",
            )
        return cv

    @staticmethod
    async def delete_cv(cv_id: int) -> bool:
        result = await CVRepository.delete(cv_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV not found",
            )
        return True