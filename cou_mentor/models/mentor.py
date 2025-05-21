from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from datetime import datetime, timezone
from cou_user.models.user import User
# from cou_user.models.course import Course
class Mentor(SQLModel, table=True):
    __tablename__ = "mentor"
    __table_args__ = {"schema": "cou_mentor"}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="cou_user.user.id")
    institute_id: Optional[int] = None
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
    
    # ✅ Using JSONB for dictionary fields (PostgreSQL)
    availability_schedule: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    additional_details: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    
    weekly_avg_hours_can_spend: Optional[int] = None
    mentor_level: Optional[str] = None
    active: Optional[bool] = True
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationship with User (Optional)
    user: Optional["User"] = Relationship(back_populates="mentor")
    
    @property
    def total_students(self) -> int:
        return sum(course.total_enrollments for course in self.user.courses) if self.user and self.user.courses else 0

    class Config:
        from_attributes = True
