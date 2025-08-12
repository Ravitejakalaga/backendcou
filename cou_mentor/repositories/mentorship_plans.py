from sqlmodel import Session, select
from cou_mentor.models.mentorship_plan import MentorshipPlan
from cou_mentor.schemas.mentorship_plan import MentorshipPlanCreate, MentorshipPlanUpdate
from typing import List, Optional,Dict

from sqlalchemy.sql import text



class MentorshipPlanRepository:

    @staticmethod
    def calculate_totals(data: MentorshipPlanCreate) -> tuple[float, float]:
        total_before = data.price_monthly * data.duration_months
        if data.discount_percent is not None:
            total_after = total_before * (1 - data.discount_percent / 100.0)
        else:
            total_after = total_before
        return total_before, total_after

    @staticmethod
    def create(session: Session, data: MentorshipPlanCreate) -> MentorshipPlan:
        total_before, total_after = MentorshipPlanRepository.calculate_totals(data)
        
        filtered_data = data.dict(exclude={"total_price_before_discount", "total_price_after_discount"})

        plan = MentorshipPlan(
            **filtered_data,
            total_price_before_discount=total_before,
            total_price_after_discount=total_after
        )
        session.add(plan)
        session.commit()
        session.refresh(plan)
        return plan
    @staticmethod
    def update(session: Session, plan_id: int, data: MentorshipPlanUpdate) -> Optional[MentorshipPlan]:
        plan = session.get(MentorshipPlan, plan_id)
        if not plan:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(plan, key, value)

        # Recalculate totals if related fields changed
        updated_data = data.dict(exclude_unset=True)
        if any(k in updated_data for k in ["price_monthly", "duration_months", "discount_percent"]):
            price = updated_data.get("price_monthly", plan.price_monthly)
            months = updated_data.get("duration_months", plan.duration_months)
            discount = updated_data.get("discount_percent", plan.discount_percent)

            total_before = price * months
            total_after = total_before * (1 - discount / 100.0) if discount is not None else total_before

            plan.total_price_before_discount = total_before
            plan.total_price_after_discount = total_after

        session.commit()
        session.refresh(plan)
        return plan
    @staticmethod
    def get_all(session: Session) -> List[MentorshipPlan]:
         return session.exec(select(MentorshipPlan)).all()

    @staticmethod
    def get_by_id(session: Session, plan_id: int) -> Optional[MentorshipPlan]:
        return session.get(MentorshipPlan, plan_id)
    @staticmethod
    def get_selected_fields_by_mentor_and_duration(session: Session, mentor_id: int, duration: int) -> List[Dict]:
        query = text("""
            SELECT 
                duration_months,
                sessions_per_week,
                referrals_included,
                curriculum_url,
                discount_percent,
                total_price_after_discount
            FROM cou_mentor.mentorship_plans
            WHERE mentor_id = :mentor_id AND duration_months = :duration
        """)
        result = session.execute(query, {
            "mentor_id": mentor_id,
            "duration": duration
        }).mappings().all()
        return [dict(row) for row in result]