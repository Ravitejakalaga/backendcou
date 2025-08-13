# cou_mentor/repositories/mentor_consultation.py
from typing import List, Optional
from sqlmodel import select, Session
import uuid
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from cou_mentor.models.mentor_consultation import MentorConsultation
from cou_mentor.schemas.mentor_consultation import MentorConsultationCreate
from cou_user.models.user import User
from cou_mentor.models.mentor import Mentor
from fastapi import HTTPException
import json

def generate_jitsi_link(mentor_id: int, mentee_id: int) -> str:
    room_name = f"mentor-{mentor_id}-mentee-{mentee_id}-{uuid.uuid4().hex[:8]}"
    return f"https://meet.jit.si/{room_name}"

class MentorConsultationRepository:

    def check_availability(self, db: Session, mentor_id: int, scheduled_time) -> bool:
        mentor = db.get(Mentor, mentor_id)
        if not mentor:
            raise HTTPException(status_code=400, detail="Mentor not found")
        
        if not mentor.availability_schedule:
            return False
        
        try:
            availability = mentor.availability_schedule
            # If stored as JSON, it's already a dict; adjust if it's a str
            if isinstance(availability, str):
                availability = json.loads(availability)

            # Example availability format:
            # {"slots": ["2025-08-10T09:00:00", "2025-08-10T14:00:00"]}
            requested_str = scheduled_time.isoformat()
            return requested_str in availability.get("slots", [])
        except Exception:
            return False

    def create(self, db: Session, data: MentorConsultationCreate) -> MentorConsultation:
        # Validate mentor exists
        mentor_exists = db.get(User, data.mentor_id)
        if not mentor_exists:
            raise HTTPException(status_code=400, detail=f"Mentor ID {data.mentor_id} does not exist")

        mentee_exists = db.get(User, data.mentee_id)
        if not mentee_exists:
            raise HTTPException(status_code=400, detail=f"Mentee ID {data.mentee_id} does not exist")

        # Check availability
        if not self.check_availability(db, data.mentor_id, data.scheduled_time):
            raise HTTPException(status_code=409, detail="Requested time slot is not available")

        # Fixed rules
        duration = 60
        expiry_time = data.scheduled_time + timedelta(minutes=60)
        meeting_url = generate_jitsi_link(data.mentor_id, data.mentee_id)

        consultation = MentorConsultation(
            **data.dict(),
            duration_minutes=duration,
            booking_status="successful",
            session_expiry_time=expiry_time,
            meeting_link=meeting_url
        )

        try:
            db.add(consultation)
            db.commit()
            db.refresh(consultation)
            return consultation
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    def get_all(self, db: Session) -> List[MentorConsultation]:
        return db.exec(select(MentorConsultation)).all()

    def get_by_id(self, db: Session, consultation_id: int) -> Optional[MentorConsultation]:
        return db.get(MentorConsultation, consultation_id)

    def delete(self, db: Session, consultation_id: int) -> Optional[MentorConsultation]:
        consultation = db.get(MentorConsultation, consultation_id)
        if consultation:
            db.delete(consultation)
            db.commit()
        return consultation

    def update(self, db: Session, consultation_id: int, update_data: MentorConsultationCreate) -> Optional[MentorConsultation]:
        consultation = db.get(MentorConsultation, consultation_id)
        if not consultation:
            return None
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(consultation, field, value)
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        return consultation
