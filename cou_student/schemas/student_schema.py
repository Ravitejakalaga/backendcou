from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class StudentBase(SQLModel):
    enrolled_courses: Optional[int]
    active_courses: Optional[int]
    completed_courses: Optional[int]

class StudentCreate(StudentBase):
    created_by: int
    user_id: Optional[int] = None

class StudentUpdate(SQLModel):
    enrolled_courses: Optional[int]
    active_courses: Optional[int]
    active: Optional[bool] = None
    

class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    active: bool
    corporate_job_experience :Optional[int] = None
    enrolled_courses: Optional[int]
    active_courses: Optional[int]
    student_level: Optional[str]
   
class Config:
    orm_mode = True