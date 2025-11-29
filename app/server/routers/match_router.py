from fastapi import APIRouter, status
from typing import List
from schemas.match_schema import MatchResultResponse
from services.match_service import MatchService

router = APIRouter(prefix="/match", tags=["match"])


@router.get("/cv/{cv_id}", response_model=List[MatchResultResponse])
async def get_cv_matches(cv_id: int):
    return await MatchService.get_cv_matches(cv_id)


@router.get("/job/{job_id}", response_model=List[MatchResultResponse])
async def get_job_matches(job_id: int):
    return await MatchService.get_job_matches(job_id)


@router.post("/recompute/cv/{cv_id}", response_model=List[MatchResultResponse])
async def recompute_cv_match(cv_id: int):
    return await MatchService.recompute_cv_match(cv_id)


@router.post("/recompute/job/{job_id}", response_model=List[MatchResultResponse])
async def recompute_job_match(job_id: int):
    return await MatchService.recompute_job_match(job_id)