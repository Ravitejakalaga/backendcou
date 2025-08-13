from sqlmodel import Session
from typing import List, Optional
from models.mentor_consultation import MentorConsultation
from schemas.mentor_consultation import MentorConsultationCreate
from repositories.mentor_consultation import MentorConsultationRepository


class MentorConsultationService:
    def __init__(self):
        self.repo = MentorConsultationRepository()

    def create_consultation(self, db: Session, consultation_data: MentorConsultationCreate) -> MentorConsultation:
        return self.repo.create(db, consultation_data)

    def get_all_consultations(self, db: Session) -> List[MentorConsultation]:
        return self.repo.get_all(db)

    def get_consultation_by_id(self, db: Session, consultation_id: int) -> Optional[MentorConsultation]:
        return self.repo.get_by_id(db, consultation_id)

    def update_consultation(self, db: Session, consultation_id: int, data: MentorConsultationCreate) -> Optional[MentorConsultation]:
        return self.repo.update(db, consultation_id, data)

    def delete_consultation(self, db: Session, consultation_id: int) -> Optional[MentorConsultation]:
        return self.repo.delete(db, consultation_id)
