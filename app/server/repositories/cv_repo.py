from typing import Optional, List
from models.candidateResume import CandidateResume


class CVRepository:
    @staticmethod
    async def create(user_id: int, title: str, location: Optional[str],
                    experience_years: int, skills: list, summary: Optional[str],
                    full_text: Optional[str], pdf_url: Optional[str],
                    is_main: bool) -> CandidateResume:
        last_cv = await CandidateResume.find().sort([("cv_id", -1)]).limit(1).to_list(1)
        cv_id = (last_cv[0].cv_id + 1) if last_cv else 1

        cv = CandidateResume(
            cv_id=cv_id,
            user_id=user_id,
            title=title,
            location=location,
            experience_years=experience_years,
            skills=skills,
            summary=summary,
            full_text=full_text,
            pdf_url=pdf_url,
            is_main=is_main,
        )
        await cv.insert()
        return cv

    @staticmethod
    async def get_by_id(cv_id: int) -> Optional[CandidateResume]:
        return await CandidateResume.find_one(CandidateResume.cv_id == cv_id)

    @staticmethod
    async def get_by_user_id(user_id: int) -> List[CandidateResume]:
        return await CandidateResume.find(CandidateResume.user_id == user_id).to_list(None)

    @staticmethod
    async def get_main_by_user_id(user_id: int) -> Optional[CandidateResume]:
        return await CandidateResume.find_one(
            (CandidateResume.user_id == user_id) & (CandidateResume.is_main == True)
        )

    @staticmethod
    async def update(cv_id: int, **kwargs) -> Optional[CandidateResume]:
        cv = await CandidateResume.find_one(CandidateResume.cv_id == cv_id)
        if cv:
            await cv.update({"$set": kwargs})
            return await CVRepository.get_by_id(cv_id)
        return None

    @staticmethod
    async def delete(cv_id: int) -> bool:
        cv = await CandidateResume.find_one(CandidateResume.cv_id == cv_id)
        if cv:
            await cv.delete()
            return True
        return False