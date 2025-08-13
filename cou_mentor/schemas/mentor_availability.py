from pydantic import BaseModel
from typing import Dict, Optional

class MentorAvailabilityResponse(BaseModel):
    mentor_id: int
    availability_schedule: Optional[Dict[str, str]]

    class Config:
        orm_mode = True
