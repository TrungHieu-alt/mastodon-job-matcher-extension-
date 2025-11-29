from typing import Optional, List
from models.application import Application


class ApplicationRepository:
    @staticmethod
    async def create(job_id: int, candidate_id: int, cv_id: int) -> Application:
        last_app = await Application.find().sort([("app_id", -1)]).limit(1).to_list(1)
        app_id = (last_app[0].app_id + 1) if last_app else 1

        app = Application(
            app_id=app_id,
            job_id=job_id,
            candidate_id=candidate_id,
            cv_id=cv_id,
            status="pending",
        )
        await app.insert()
        return app

    @staticmethod
    async def get_by_id(app_id: int) -> Optional[Application]:
        return await Application.find_one(Application.app_id == app_id)

    @staticmethod
    async def get_by_job_id(job_id: int) -> List[Application]:
        return await Application.find(Application.job_id == job_id).to_list(None)

    @staticmethod
    async def get_by_candidate_id(candidate_id: int) -> List[Application]:
        return await Application.find(Application.candidate_id == candidate_id).to_list(None)

    @staticmethod
    async def update(app_id: int, **kwargs) -> Optional[Application]:
        app = await Application.find_one(Application.app_id == app_id)
        if app:
            await app.update({"$set": kwargs})
            return await ApplicationRepository.get_by_id(app_id)
        return None

    @staticmethod
    async def delete(app_id: int) -> bool:
        app = await Application.find_one(Application.app_id == app_id)
        if app:
            await app.delete()
            return True
        return False