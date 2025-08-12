from sqlmodel import SQLModel, Field,Relationship , Column, Float 
from typing import Optional,TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Computed

if TYPE_CHECKING:
    from cou_mentor.models.mentor import Mentor

class MentorshipPlan(SQLModel, table=True):
    __tablename__ = "mentorship_plans"
    __table_args__ = {"schema": "cou_mentor"}

    id: Optional[int] = Field(default=None, primary_key=True)
    mentor_id: int = Field(foreign_key="cou_mentor.mentor.id")
    plan_name: str
    duration_months: int
    sessions_per_week: int
    price_monthly: float
    discount_percent: Optional[float] = None
    currency_code: str = Field(default="USD", max_length=3)
    referrals_included: Optional[str] = None
    curriculum_url: Optional[str] = None
    sessions_description: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    total_price_before_discount: Optional[float] = Field(
        sa_column=Column(
            "total_price_before_discount",
            Float,
            Computed("price_monthly * duration_months", persisted=True)
        )
    )

    total_price_after_discount: Optional[float] = Field(
        sa_column=Column(
            "total_price_after_discount",
            Float,
            Computed(
                """
                CASE 
                    WHEN discount_percent IS NULL THEN price_monthly * duration_months
                    ELSE (price_monthly * duration_months) * (1 - discount_percent / 100.0)
                END
                """,
                persisted=True
            )
        )
    )


    mentor: list["Mentor"] = Relationship(
        back_populates="mentorship_plans",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    