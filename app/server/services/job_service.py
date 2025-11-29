from typing import Optional, List
from fastapi import HTTPException, status
from repositories.job_repo import JobRepository
from models.jobPost import JobPost


class JobService:
    @staticmethod
    async def create_job(recruiter_id: int, title: str, role: str, location: str,
                        job_type: str, experience_level: str, skills: list,
                        salary_min: Optional[float], salary_max: Optional[float],
                        full_text: Optional[str], pdf_url: Optional[str]) -> JobPost:
        return await JobRepository.create(recruiter_id, title, role, location, job_type,
                                         experience_level, skills, salary_min, salary_max, full_text, pdf_url)

    @staticmethod
    async def get_job(job_id: int) -> Optional[JobPost]:
        job = await JobRepository.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return job

    @staticmethod
    async def get_all_jobs() -> List[JobPost]:
        return await JobRepository.get_all()

    @staticmethod
    async def update_job(job_id: int, **kwargs) -> Optional[JobPost]:
        job = await JobRepository.update(job_id, **kwargs)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return job

    @staticmethod
    async def delete_job(job_id: int) -> bool:
        result = await JobRepository.delete(job_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return True