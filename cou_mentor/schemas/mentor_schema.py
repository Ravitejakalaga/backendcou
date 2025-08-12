from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
 
class MentorBase(BaseModel):
    user_id: int
    institute_id: Optional[int] = None
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
 
    tutoring: Optional[bool] = False
    mentoring_one_one: Optional[bool] = False
    project_assistance: Optional[bool] = False
    mock_interviews: Optional[bool] = False
    create_brand: Optional[bool] = False
    sell_content: Optional[bool] = False
    travel_ready: Optional[bool] = False
 
    availability_schedule: Optional[Dict[str, Any]] = None
    additional_details: Optional[Dict[str, Any]] = None
    weekly_avg_hours_can_spend: Optional[int] = None
    mentor_level: Optional[str] = None
    active: Optional[bool] = True
    expertise: Optional[str] = None
    mentor_about: Optional[str] = None
    mentor_intro: Optional[str] = None
    open_for_inquires: Optional[bool] = None
    offering_mentorship_for: Optional[str] = None
    companies: Optional[str] = None
    designation: Optional[str] = None
 
 
class MentorCreate(MentorBase):
    created_by: int
    updated_by: int
 
 
class MentorUpdate(BaseModel):
    bio: Optional[str] = None
    overall_experience: Optional[int] = None
    teaching_experience: Optional[int] = None
    corporate_training_exp: Optional[int] = None
    is_parttime: Optional[bool] = None
    cloudou_rating: Optional[float] = None
    avg_students_rating: Optional[float] = None
    hourly_rate: Optional[float] = None
    weekly_rate: Optional[float] = None
    monthly_rate: Optional[float] = None
 
    tutoring: Optional[bool] = None
    mentoring_one_one: Optional[bool] = None
    project_assistance: Optional[bool] = None
    mock_interviews: Optional[bool] = None
    create_brand: Optional[bool] = None
    sell_content: Optional[bool] = None
    travel_ready: Optional[bool] = None
 
    availability_schedule: Optional[Dict[str, Any]] = None
    additional_details: Optional[Dict[str, Any]] = None
    weekly_avg_hours_can_spend: Optional[int] = None
    mentor_level: Optional[str] = None
    active: Optional[bool] = None
    expertise: Optional[str] = None
    mentor_about: Optional[str] = None
    mentor_intro: Optional[str] = None
    open_for_inquires: Optional[bool] = None
    offering_mentorship_for: Optional[str] = None
    companies: Optional[str] = None
    designation: Optional[str] = None
    updated_by: Optional[int] = None
 
 

    
class MentorRead(MentorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
 
    class Config:
        from_attributes = True