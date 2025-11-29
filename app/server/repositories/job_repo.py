from typing import Optional, List
from models.jobPost import JobPost


class JobRepository:
    @staticmethod
    async def create(recruiter_id: int, title: str, role: str, location: str,
                    job_type: str, experience_level: str, skills: list,
                    salary_min: Optional[float], salary_max: Optional[float],
                    full_text: Optional[str], pdf_url: Optional[str]) -> JobPost:
        last_job = await JobPost.find().sort([("job_id", -1)]).limit(1).to_list(1)
        job_id = (last_job[0].job_id + 1) if last_job else 1

        job = JobPost(
            job_id=job_id,
            recruiter_id=recruiter_id,
            title=title,
            role=role,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            skills=skills,
            salary_min=salary_min,
            salary_max=salary_max,
            full_text=full_text,
            pdf_url=pdf_url,
        )
        await job.insert()
        return job

    @staticmethod
    async def get_by_id(job_id: int) -> Optional[JobPost]:
        return await JobPost.find_one(JobPost.job_id == job_id)

    @staticmethod
    async def get_all() -> List[JobPost]:
        return await JobPost.find().to_list(None)

    @staticmethod
    async def update(job_id: int, **kwargs) -> Optional[JobPost]:
        job = await JobPost.find_one(JobPost.job_id == job_id)
        if job:
            await job.update({"$set": kwargs})
            return await JobRepository.get_by_id(job_id)
        return None

    @staticmethod
    async def delete(job_id: int) -> bool:
        job = await JobPost.find_one(JobPost.job_id == job_id)
        if job:
            await job.delete()
            return True
        return False