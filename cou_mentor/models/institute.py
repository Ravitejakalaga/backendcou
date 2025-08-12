from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime

if TYPE_CHECKING:
    from .mentor import Mentor

class Institute(SQLModel, table=True):
    __tablename__ = "institute"
    __table_args__ = {"schema": "cou_mentor"}

    id: Optional[int] = Field(default=None, primary_key=True)
    institute_name: str = Field(index=True, nullable=False, max_length=255)
    description: Optional[str] = None
    no_of_students: Optional[int] = None
    no_of_teachers: Optional[int] = None
    ranking: Optional[int] = None
    address: Optional[str] = None
    is_popular: Optional[bool] = Field(default=False)
    is_private: Optional[bool] = Field(default=False)
    is_university: Optional[bool] = Field(default=False)
    is_library: Optional[bool] = Field(default=False)
    is_school: Optional[bool] = Field(default=False)
    city_id: Optional[int] = Field(default=None, foreign_key="cou_admin.city.id")
    zip_id: Optional[int] = Field(default=None, foreign_key="cou_admin.zip.id")
    affiliate_information: Optional[dict] = Field(default=None, sa_type=JSON)
    website_url: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: int
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_by: int
    active: Optional[bool] = Field(default=True)
    
    
    
    mentors: List["Mentor"] = Relationship(back_populates="institute")
 
