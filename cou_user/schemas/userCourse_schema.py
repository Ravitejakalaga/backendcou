from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel

class UserCourseCreate(SQLModel):
    user_id: Optional[int]
    course_id: Optional[int]
    transaction_id: Optional[UUID]
    is_enrolled: Optional[bool] = False
    enrollment_date: Optional[datetime]
    course_completion_status: Optional[str]
    created_by: Optional[int]
    updated_by: Optional[int]
    active: Optional[bool] = True
    price: Optional[float] = 0

class UserCourseRead(SQLModel):
    id: int
    user_id: Optional[int]
    course_id: Optional[int]
    transaction_id: Optional[UUID]
    cart_date: Optional[datetime]
    is_enrolled: bool
    enrollment_date: Optional[datetime]
    course_completion_status: Optional[str]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    active: bool

class UserCourseDetailRead(BaseModel):
    # UserCourse fields
    id: int
    user_id: int
    course_id: int
    transaction_id: Optional[UUID]
    cart_date: Optional[datetime]
    is_enrolled: bool
    enrollment_date: Optional[datetime]
    course_completion_status: Optional[str]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    active: bool
    
    # Course fields
    course_title: str
    course_description: Optional[str]
    course_category_id: Optional[int]
    course_subcategory_id: Optional[int]
    course_type_id: Optional[int]
    course_sells_type_id: Optional[int]
    course_mentor_id: Optional[int]
    course_language_id: Optional[int]
    course_created_at: datetime
    course_updated_at: datetime
    course_is_flagship: Optional[bool]
    course_active: Optional[bool]
    course_price: Optional[float]
    
    class Config:
        orm_mode = True


