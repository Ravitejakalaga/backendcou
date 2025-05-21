from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class MentorBase(BaseModel):
    user_id: int
    bio: Optional[str] = None
    overall_experience: Optional[int] = None
    teaching_experience: Optional[int] = None
    corporate_training_exp: Optional[int] = None
    is_parttime: Optional[bool] = False
    cloudou_rating: Optional[float] = None
    avg_students_rating: Optional[float] = None
    hourly_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
    mentor_level: Optional[str] = None
    additional_details: Optional[Dict[str, Any]] = None
    availability_schedule: Optional[Dict[str, Any]] = None
    active: Optional[bool] = True

class MentorCreate(MentorBase):
    pass

class MentorUpdate(BaseModel):
    bio: Optional[str] = None
    overall_experience: Optional[int] = None
    teaching_experience: Optional[int] = None
    corporate_training_exp: Optional[int] = None
    is_parttime: Optional[bool] = False
    cloudou_rating: Optional[float] = None
    avg_students_rating: Optional[float] = None
    hourly_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
    mentor_level: Optional[str] = None
    additional_details: Optional[Dict[str, Any]] = None
    availability_schedule: Optional[Dict[str, Any]] = None
    active: Optional[bool] = True

class MentorRead(MentorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
