# cou_mentor/api/mentor_consultation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from common.database import get_session
from cou_mentor.schemas.mentor_consultation import MentorConsultationCreate, MentorConsultationRead
from cou_mentor.repositories.mentor_consultation import MentorConsultationRepository

router = APIRouter(prefix="/mentor-consultations", tags=["Mentor Consultations"])
repo = MentorConsultationRepository()

@router.post("/", response_model=MentorConsultationRead)
def create_consultation(data: MentorConsultationCreate, db: Session = Depends(get_session)):
    return repo.create(db, data)

@router.get("/", response_model=list[MentorConsultationRead])
def get_all_consultations(db: Session = Depends(get_session)):
    return repo.get_all(db)

@router.get("/{consultation_id}", response_model=MentorConsultationRead)
def get_consultation(consultation_id: int, db: Session = Depends(get_session)):
    consultation = repo.get_by_id(db, consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation

@router.delete("/{consultation_id}")
def delete_consultation(consultation_id: int, db: Session = Depends(get_session)):
    deleted = repo.delete(db, consultation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return {"message": "Consultation deleted successfully"}

@router.put("/{consultation_id}", response_model=MentorConsultationRead)
def update_consultation(consultation_id: int, data: MentorConsultationCreate, db: Session = Depends(get_session)):
    updated = repo.update(db, consultation_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return updated
