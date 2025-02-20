from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from cou_user.models.user import User


class Mentor(SQLModel, table=True):
    __tablename__ = "mentor"
    __table_args__ = {"schema": "cou_user"}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="cou_user.user.id", unique=True)
    bio: Optional[str] = None
    expertise: Optional[str] = Field(default=None, max_length=500)
    rating: Optional[float] = Field(default=0.0)
    is_available: Optional[bool] = Field(default=True)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user: Optional["User"] = Relationship(back_populates="mentor")
    
    @property
    def total_students(self) -> int:
        return sum(course.total_enrollments for course in self.user.courses) if self.user and self.user.courses else 0