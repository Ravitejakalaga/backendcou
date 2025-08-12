from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MentorshipPlanCreate(BaseModel):
    mentor_id: int
    plan_name: str
    duration_months: int
    sessions_per_week: int
    price_monthly: float
    discount_percent: Optional[float] = None
    currency_code: Optional[str] = "USD"
    referrals_included: Optional[str] = None
    curriculum_url: Optional[str] = None
    sessions_description: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    total_price_before_discount: Optional[float]
    total_price_after_discount: Optional[float]

class MentorshipPlanRead(MentorshipPlanCreate):
    mentor_id: int
    plan_name: str
    duration_months: int
    sessions_per_week: int
    price_monthly: float
    discount_percent: Optional[float] = None
    currency_code: Optional[str] = "USD"
    referrals_included: Optional[str] = None
    curriculum_url: Optional[str] = None
    sessions_description: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    total_price_before_discount: Optional[float]
    total_price_after_discount: Optional[float]


class MentorshipPlanUpdate(BaseModel):
    mentor_id: int
    plan_name: str
    duration_months: int
    sessions_per_week: int
    price_monthly: float
    discount_percent: Optional[float] = None
    currency_code: Optional[str] = "USD"
    referrals_included: Optional[str] = None
    curriculum_url: Optional[str] = None
    sessions_description: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    total_price_before_discount: Optional[float]
    total_price_after_discount: Optional[float]
