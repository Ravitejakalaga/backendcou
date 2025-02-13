from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.database import get_session
from ..repositories.onboarding_progress_repository import OnboardingProgressRepository
from ..schemas.onboarding_progress_schema import (
    OnboardingProgressCreate,
    OnboardingProgressUpdate,
    OnboardingProgressResponse
)

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])
repository = OnboardingProgressRepository()

@router.post("", response_model=OnboardingProgressResponse)
def create_onboarding_progress(
    onboarding: OnboardingProgressCreate,
    db: Session = Depends(get_session)
):
    return repository.create(db, onboarding)

@router.get("/{session_id}", response_model=OnboardingProgressResponse)
def get_onboarding_progress(
    session_id: UUID,
    db: Session = Depends(get_session)
):
    db_onboarding = repository.get_by_session_id(db, session_id)
    if not db_onboarding:
        raise HTTPException(status_code=404, detail="Onboarding progress not found")
    return db_onboarding

@router.get("/user/{user_id}", response_model=List[OnboardingProgressResponse])
def get_user_onboarding_progress(
    user_id: UUID,
    db: Session = Depends(get_session)
):
    return repository.get_by_user_id(db, user_id)

@router.get("", response_model=List[OnboardingProgressResponse])
def get_all_onboarding_progress(
    db: Session = Depends(get_session)
):
    return repository.get_all(db)

@router.put("/{session_id}", response_model=OnboardingProgressResponse)
def update_onboarding_progress(
    session_id: UUID,
    onboarding: OnboardingProgressUpdate,
    db: Session = Depends(get_session)
):
    db_onboarding = repository.update(db, session_id, onboarding)
    if not db_onboarding:
        raise HTTPException(status_code=404, detail="Onboarding progress not found")
    return db_onboarding

@router.delete("/{session_id}")
def delete_onboarding_progress(
    session_id: UUID,
    db: Session = Depends(get_session)
):
    if not repository.delete(db, session_id):
        raise HTTPException(status_code=404, detail="Onboarding progress not found")
    return {"message": "Onboarding progress deleted successfully"} 