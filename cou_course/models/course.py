from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from cou_user.models.user import User

class Course(SQLModel, table=True):
    __tablename__ = "course"
    __table_args__ = {"schema": "cou_course"}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    what_will_you: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="cou_course.course_category.id")
    subcategory_id: Optional[int] = Field(default=None, foreign_key="cou_course.course_subcategory.id")
    course_type_id: Optional[int] = Field(default=None, foreign_key="cou_course.course_type.id")
    sells_type_id: Optional[int] = Field(default=None, foreign_key="cou_course.sells_type.id")
    mentor_id: Optional[int] = Field(default=None, foreign_key="cou_user.user.id")
    language_id: Optional[int] = Field(default=None, foreign_key="cou_admin.language.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_flagship: Optional[bool] = Field(default=False)
    active: Optional[bool] = Field(default=True)
    price: Optional[float] = Field(default=0.0)
    ratings: Optional[int] = None
    slug: Optional[str] = None
    discount: Optional[float] = None
    introduction_video: Optional[str] = None
    prerequisites: Optional[str] = None
    skill_level: Optional[str] = None
    max_students: Optional[float] = None
    thumbnail: Optional[str] = None
    time: Optional[float] = None
    is_live: Optional[bool] = None
    instructor: Optional["User"] = Relationship(
        back_populates="courses",
        sa_relationship_kwargs={"lazy": "joined"}
    )
