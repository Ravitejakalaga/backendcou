from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class JobRoleBase(BaseModel):
    job_role_name: str
    description: Optional[str] = None
    category_id: int
    subcategory_id: int
    active: bool = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "job_role_name": "Senior Software Engineer",
                "description": "Lead software engineer position with full-stack development responsibilities",
                "category_id": 1,
                "subcategory_id": 2,
                "active": True
            }
        }

class JobRoleCreate(JobRoleBase):
    created_by: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "job_role_name": "Senior Software Engineer",
                "description": "Lead software engineer position with full-stack development responsibilities",
                "category_id": 1,
                "subcategory_id": 2,
                "active": True,
                "created_by": 1
            }
        }

class JobRoleUpdate(BaseModel):
    job_role_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    active: Optional[bool] = None
    updated_by: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "job_role_name": "Lead Software Engineer",
                "description": "Updated role description for lead software engineer position",
                "category_id": 1,
                "subcategory_id": 3,
                "active": True,
                "updated_by": 1
            }
        }

class JobRoleInDB(JobRoleBase):
    id: int
    created_at: datetime
    created_by: int
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "job_role_name": "Senior Software Engineer",
                "description": "Lead software engineer position with full-stack development responsibilities",
                "category_id": 1,
                "subcategory_id": 2,
                "active": True,
                "created_at": "2024-02-14T12:00:00Z",
                "created_by": 1,
                "updated_at": "2024-02-14T13:00:00Z",
                "updated_by": 2
            }
        } 