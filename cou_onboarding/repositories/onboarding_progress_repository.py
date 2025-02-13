from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.onboarding_progress import OnboardingProgress
from ..schemas.onboarding_progress_schema import OnboardingProgressCreate, OnboardingProgressUpdate

class OnboardingProgressRepository:
    def create(self, db: Session, onboarding: OnboardingProgressCreate) -> OnboardingProgress:
        db_onboarding = OnboardingProgress(**onboarding.model_dump(exclude_unset=True))
        db.add(db_onboarding)
        db.commit()
        db.refresh(db_onboarding)
        return db_onboarding

    def get_by_session_id(self, db: Session, session_id: UUID) -> Optional[OnboardingProgress]:
        return db.query(OnboardingProgress).filter(OnboardingProgress.session_id == session_id).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> List[OnboardingProgress]:
        return db.query(OnboardingProgress).filter(OnboardingProgress.user_id == user_id).all()

    def get_all(self, db: Session) -> List[OnboardingProgress]:
        return db.query(OnboardingProgress).all()

    def update(self, db: Session, session_id: UUID, onboarding: OnboardingProgressUpdate) -> Optional[OnboardingProgress]:
        db_onboarding = self.get_by_session_id(db, session_id)
        if db_onboarding:
            update_data = onboarding.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_onboarding, key, value)
            db.commit()
            db.refresh(db_onboarding)
        return db_onboarding

    def delete(self, db: Session, session_id: UUID) -> bool:
        db_onboarding = self.get_by_session_id(db, session_id)
        if db_onboarding:
            db.delete(db_onboarding)
            db.commit()
            return True
        return False 