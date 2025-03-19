from sqlmodel import SQLModel, Field , Relationship
from typing import Optional
from datetime import datetime , timezone
from uuid import UUID

class UserCourse(SQLModel, table=True):
    __tablename__ = "user_course"
    __table_args__ = {"schema": "cou_user"}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="cou_user.user.id")
    course_id: Optional[int] = Field(default=None, foreign_key="cou_course.course.id")
    transaction_id: Optional[UUID] = None
    cart_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_enrolled: bool = Field(default=False)
    enrollment_date: Optional[datetime] = None
    course_completion_status: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    active: bool = Field(default=True)
    price: Optional[float] = Field(default=0)