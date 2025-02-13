from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class JobRole(SQLModel, table=True):
    __tablename__ = "job_role"
    __table_args__ = {"schema": "cou_user"}

    id: Optional[int] = Field(default=None, primary_key=True)
    job_role_name: str
    description: Optional[str] = None
    category_id: int
    subcategory_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: int
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: int
    active: bool = Field(default=True) 