from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Field, SQLModel
from sqlalchemy import text, Column, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID as pgUUID

class OnboardingProgress(SQLModel, table=True):
    __tablename__ = "onboarding_progress"
    __table_args__ = {"schema": "public"}

    session_id: UUID = Field(
        default=None,
        sa_column=Column(pgUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    )
    step_number: Optional[int] = Field(default=None)
    data: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    user_id: Optional[UUID] = Field(
        default=None,
        sa_column=Column(pgUUID(as_uuid=True))
    ) 