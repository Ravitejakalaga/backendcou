from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional

class UserSkills(SQLModel, table=True):
    __tablename__ = "user_skills"
    __table_args__ = {"schema": "cou_user"}
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    certification: Optional[str]
    created_by: int
    updated_by: int
    current_skills: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=True))
    target_skills: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=True))
    recent_search: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=True))
