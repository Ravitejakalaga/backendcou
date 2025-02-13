from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class JobRoleBase(BaseModel):
    job_role_name: str
    description: Optional[str] = None
    category_id: int
    subcategory_id: int
    active: bool = True

class JobRoleCreate(JobRoleBase):
    created_by: int

class JobRoleUpdate(BaseModel):
    job_role_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    active: Optional[bool] = None
    updated_by: int

class JobRoleInDB(JobRoleBase):
    id: int
    created_at: datetime
    created_by: int
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True 