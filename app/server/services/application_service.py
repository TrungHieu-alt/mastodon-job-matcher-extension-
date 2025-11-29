from typing import Optional, List
from fastapi import HTTPException, status
from repositories.application_repo import ApplicationRepository
from models.application import Application


class ApplicationService:
    @staticmethod
    async def create_application(job_id: int, candidate_id: int, cv_id: int) -> Application:
        return await ApplicationRepository.create(job_id, candidate_id, cv_id)

    @staticmethod
    async def get_application(app_id: int) -> Optional[Application]:
        app = await ApplicationRepository.get_by_id(app_id)
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )
        return app

    @staticmethod
    async def get_job_applications(job_id: int) -> List[Application]:
        return await ApplicationRepository.get_by_job_id(job_id)

    @staticmethod
    async def get_candidate_applications(candidate_id: int) -> List[Application]:
        return await ApplicationRepository.get_by_candidate_id(candidate_id)

    @staticmethod
    async def update_application(app_id: int, **kwargs) -> Optional[Application]:
        app = await ApplicationRepository.update(app_id, **kwargs)
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )
        return app

    @staticmethod
    async def delete_application(app_id: int) -> bool:
        result = await ApplicationRepository.delete(app_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )
        return True