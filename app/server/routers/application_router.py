from fastapi import APIRouter, status, Query
from typing import List
from schemas.application_schema import ApplicationRequest, ApplicationUpdateRequest, ApplicationResponse
from services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ApplicationResponse)
async def create_application(user_id: int = Query(...), req: ApplicationRequest = None):
    app = await ApplicationService.create_application(req.job_id, user_id, req.cv_id)
    return app


@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
async def get_job_applications(job_id: int):
    return await ApplicationService.get_job_applications(job_id)


@router.get("/candidate/{user_id}", response_model=List[ApplicationResponse])
async def get_candidate_applications(user_id: int):
    return await ApplicationService.get_candidate_applications(user_id)


@router.put("/{app_id}", response_model=ApplicationResponse)
async def update_application(app_id: int, req: ApplicationUpdateRequest):
    app = await ApplicationService.update_application(app_id, status=req.status)
    return app


@router.delete("/{app_id}", status_code=status.HTTP_200_OK)
async def delete_application(app_id: int):
    await ApplicationService.delete_application(app_id)
    return {"message": "Application deleted"}