from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import text, Column, DateTime, JSON
from typing import Dict, Any
import json



class Student(SQLModel, table=True):
    __tablename__ = "student"
    __table_args__ = {"schema": "cou_student"}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="cou_user.user.id")
    enrolled_courses: Optional[int] = None
    active_courses: Optional[int] = None
    completed_courses: Optional[int] = None
    is_fresher: Optional[bool] = Field(default=False)
    overall_experience: Optional[int] = None
    corporate_job_experience: Optional[int] = None
    need_job: Optional[bool] = Field(default=False)
    better_salary: Optional[bool] = Field(default=False)
    pursuing: Optional[bool] = Field(default=False)
    cloudou_rating: Optional[Decimal] = Field(None, ge=0, le=9.99, description="rating in numbers with a max of 3 digits and 2 decimal places.")
    avg_mentors_rating: Optional[Decimal] = Field(None, ge=0, le=9.99, description="rating in numbers with a max of 3 digits and 2 decimal places.")
    min_budget_h: Optional[Decimal] = Field(None, ge=0, le=99999999.99, description="Budget in numbers with a max of 10 digits and 2 decimal places.")
    max_budget_h: Optional[Decimal] = Field(None, ge=0, le=99999999.99, description="Budget in numbers with a max of 10 digits and 2 decimal places.")
    budget_spent: Optional[Decimal] = Field(None, ge=0, le=99999999.99, description="rating in numbers with a max of 3 digits and 2 decimal places.")
    student_level: Optional[str] = Field(max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: int
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: int
    active: Optional[bool] = Field(default=True)
    additional_details: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    #additional_details: Dict[str, Any] = Field(default=None, sa_column=Field(sa_type=JSONB))

    

"""@property
def additional_details_dict(self) -> Optional[Dict[str, Any]]:
    if self.additional_details:
        return json.loads(self.additional_details)
    return None
    
@additional_details_dict.setter
def additional_details_dict(self, value: Optional[Dict[str, Any]]):
    if value is not None:
        self.additional_details = json.dumps(value)
    else:
        self.additional_details = None"""



