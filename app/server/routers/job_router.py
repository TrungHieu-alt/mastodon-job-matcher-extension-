from fastapi import APIRouter, status
from typing import List
from schemas.job_schema import JobPostRequest, JobPostResponse
from services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/create/{recruiter_id}", status_code=status.HTTP_201_CREATED, response_model=JobPostResponse)
async def create_job(recruiter_id: int, req: JobPostRequest):
    job = await JobService.create_job(
        recruiter_id, req.title, req.role, req.location, req.job_type,
        req.experience_level, req.skills, req.salary_min, req.salary_max, req.full_text, req.pdf_url
    )
    return job


@router.get("", response_model=List[JobPostResponse])
async def get_all_jobs():
    return await JobService.get_all_jobs()


@router.get("/{job_id}", response_model=JobPostResponse)
async def get_job(job_id: int):
    return await JobService.get_job(job_id)


@router.put("/{job_id}", response_model=JobPostResponse)
async def update_job(job_id: int, req: JobPostRequest):
    job = await JobService.update_job(
        job_id,
        title=req.title,
        role=req.role,
        location=req.location,
        job_type=req.job_type,
        experience_level=req.experience_level,
        skills=req.skills,
        salary_min=req.salary_min,
        salary_max=req.salary_max,
        full_text=req.full_text,
        pdf_url=req.pdf_url,
    )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(job_id: int):
    await JobService.delete_job(job_id)
    return {"message": "Job deleted"}