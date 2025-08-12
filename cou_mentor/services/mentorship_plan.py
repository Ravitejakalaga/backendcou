from sqlmodel import Session
from cou_mentor.schemas.mentorship_plan import MentorshipPlanCreate, MentorshipPlanUpdate
from cou_mentor.repositories.mentorship_plans import MentorshipPlanRepository
from typing import List, Dict


class MentorshipPlanService:

    @staticmethod
    def create(session: Session, data: MentorshipPlanCreate):
        return MentorshipPlanRepository.create(session, data)

    @staticmethod
    def get_all(session: Session):
        return MentorshipPlanRepository.get_all(session)

    @staticmethod
    def get_by_id(session: Session, plan_id: int):
        return MentorshipPlanRepository.get_by_id(session, plan_id)

    @staticmethod
    def update(session: Session, plan_id: int, data: MentorshipPlanUpdate):
        return MentorshipPlanRepository.update(session, plan_id, data)

    @staticmethod
    def delete(session: Session, plan_id: int):
        return MentorshipPlanRepository.delete(session, plan_id)
    @staticmethod
    def fetch_selected_fields_by_mentor_and_duration(session: Session, mentor_id: int, duration: int) -> List[Dict]:
        return MentorshipPlanRepository.get_selected_fields_by_mentor_and_duration(session, mentor_id, duration)