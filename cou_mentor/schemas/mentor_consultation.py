from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MentorConsultationCreate(BaseModel):
    mentor_id: int
    mentee_id: int
    scheduled_time: datetime
    duration_minutes: int
    booking_status: Optional[str] = "pending"
    mentor_notes: Optional[str] = None
    feedback_rating: Optional[int] = None
    feedback_comments: Optional[str] = None
    session_expiry_time: Optional[datetime] = None
    course_id: Optional[int] = None
    is_paid: Optional[bool] = None
    price: Optional[float] = None
    payment_status: Optional[str] = None
    preparation_time: Optional[int] = None
    budget: Optional[float] = None
    mentee_requirement: Optional[str] = None
    mentor_prerequisites: Optional[str] = None
    created_by: int
    updated_by: Optional[int] = None
    active: Optional[bool] = True


class MentorConsultationRead(MentorConsultationCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    meeting_link: Optional[str]  # ✅ this is important
