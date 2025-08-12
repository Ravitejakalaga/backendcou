from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime, timezone
 
if TYPE_CHECKING:
    from .mentorship_plan import MentorshipPlan
    from cou_user.models.user import User
    from .institute import Institute
 
class Mentor(SQLModel, table=True):
    __tablename__ = "mentor"
    __table_args__ = {"schema": "cou_mentor"}
 
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="cou_user.user.id")
    institute_id: Optional[int] = Field(default=None, foreign_key="cou_mentor.institute.id")
 
    overall_experience: Optional[int] = None
    teaching_experience: Optional[int] = None
    corporate_training_exp: Optional[int] = None
 
    is_parttime: Optional[bool] = False
    cloudou_rating: Optional[float] = None
    avg_students_rating: Optional[float] = None
 
    hourly_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
 
    tutoring: Optional[bool] = False
    mentoring_one_one: Optional[bool] = False
    project_assistance: Optional[bool] = False
    mock_interviews: Optional[bool] = False
    create_brand: Optional[bool] = False
    sell_content: Optional[bool] = False
    travel_ready: Optional[bool] = False
 
    bio: Optional[str] = None
    availability_schedule: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    additional_details: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
 
    weekly_avg_hours_can_spend: Optional[int] = None
    mentor_level: Optional[str] = None
    expertise: Optional[str] = None
    mentor_about: Optional[str] = None
    mentor_intro: Optional[str] = None
    open_for_inquires: Optional[bool] = None
    offering_mentorship_for: Optional[str] = None
    companies: Optional[str] = None
    designation: Optional[str] = None
 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: int
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: int
    active: Optional[bool] = True
 
    # Relationships
    user: Optional["User"] = Relationship(back_populates="mentor")
    mentorship_plans: List["MentorshipPlan"] = Relationship(
        back_populates="mentor",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    institute: Optional["Institute"] = Relationship(back_populates="mentors")
 
    class Config:
        from_attributes = True