
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class MentorConsultation(SQLModel, table=True):
    __tablename__ = "mentor_consultation"
    __table_args__ = {"schema": "cou_mentor"}

    id: Optional[int] = Field(default=None, primary_key=True)
    mentor_id: int = Field(foreign_key="cou_mentor.mentor.id")
    mentee_id: int = Field(foreign_key="cou_user.user.id")
    scheduled_time: datetime
    duration_minutes: int
    booking_status: str = Field(default="pending", max_length=20)
    mentor_notes: Optional[str] = None
    feedback_rating: Optional[int] = None
    feedback_comments: Optional[str] = None
    session_expiry_time: Optional[datetime] = None
    course_id: Optional[int] = Field(default=None, foreign_key="cou_course.course.id")
    is_paid: Optional[bool] = None
    price: Optional[float] = Field(default=None)
    payment_status: Optional[str] = Field(default=None, max_length=50)
    meeting_link: Optional[str] = None
    preparation_time: Optional[int] = None
    budget: Optional[float] = Field(default=None)
    mentee_requirement: Optional[str] = None
    mentor_prerequisites: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = None
    active: Optional[bool] = Field(default=True)
