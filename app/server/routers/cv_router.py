from fastapi import APIRouter, status
from typing import List
from schemas.cv_schema import CandidateResumeRequest, CandidateResumeResponse
from services.cv_service import CVService

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("/create/{user_id}", status_code=status.HTTP_201_CREATED, response_model=CandidateResumeResponse)
async def create_cv(user_id: int, req: CandidateResumeRequest):
    cv = await CVService.create_cv(
        user_id, req.title, req.location, req.experience_years, req.skills,
        req.summary, req.full_text, req.pdf_url, req.is_main
    )
    return cv


@router.get("/{cv_id}", response_model=CandidateResumeResponse)
async def get_cv(cv_id: int):
    return await CVService.get_cv(cv_id)


@router.get("/user/{user_id}", response_model=List[CandidateResumeResponse])
async def get_user_cvs(user_id: int):
    return await CVService.get_user_cvs(user_id)


@router.get("/main/user/{user_id}", response_model=CandidateResumeResponse)
async def get_main_cv(user_id: int):
    return await CVService.get_main_cv(user_id)


@router.put("/{cv_id}", response_model=CandidateResumeResponse)
async def update_cv(cv_id: int, req: CandidateResumeRequest):
    cv = await CVService.update_cv(
        cv_id,
        title=req.title,
        location=req.location,
        experience_years=req.experience_years,
        skills=req.skills,
        summary=req.summary,
        full_text=req.full_text,
        pdf_url=req.pdf_url,
        is_main=req.is_main,
    )
    return cv


@router.delete("/{cv_id}", status_code=status.HTTP_200_OK)
async def delete_cv(cv_id: int):
    await CVService.delete_cv(cv_id)
    return {"message": "CV deleted"}