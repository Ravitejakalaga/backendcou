from datetime import datetime
from typing import Optional, Dict, Any, Union, List
from uuid import UUID
from sqlmodel import SQLModel, Field

class OnboardingProgressBase(SQLModel):
    step_number: Optional[int] = Field(default=None)
    data: Optional[Dict[str, Any]] = Field(default=None)  # Accepts JSON object with any valid JSON values
    user_id: Optional[UUID] = Field(default=None)  # Explicitly nullable

class OnboardingProgressCreate(OnboardingProgressBase):
    pass

class OnboardingProgressUpdate(OnboardingProgressBase):
    pass

class OnboardingProgressResponse(OnboardingProgressBase):
    session_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 