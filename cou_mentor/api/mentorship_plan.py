from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import Session
from typing import List, Dict
from common.database import get_session
 
from cou_mentor.schemas.mentorship_plan import MentorshipPlanCreate, MentorshipPlanRead, MentorshipPlanUpdate
from cou_mentor.services.mentorship_plan import MentorshipPlanService

router = APIRouter(prefix="/mentorship-plans", tags=["Mentorship Plans"])

@router.post("/", response_model=MentorshipPlanRead)
def create_plan(plan: MentorshipPlanCreate, session: Session = Depends(get_session)):
    return MentorshipPlanService.create(session, plan)

@router.get("/", response_model=list[MentorshipPlanRead])
def get_all_plans(session: Session = Depends(get_session)):
    return MentorshipPlanService.get_all(session)

@router.get("/{plan_id}", response_model=MentorshipPlanRead)
def get_plan(plan_id: int, session: Session = Depends(get_session)):
    plan = MentorshipPlanService.get_by_id(session, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.put("/{plan_id}", response_model=MentorshipPlanRead)
def update_plan(plan_id: int, update_data: MentorshipPlanUpdate, session: Session = Depends(get_session)):
    plan = MentorshipPlanService.update(session, plan_id, update_data)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, session: Session = Depends(get_session)):
    success = MentorshipPlanService.delete(session, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}

@router.get("/mentorship-plans/selected-fields", response_model=List[Dict])
def get_selected_fields_by_duration_and_mentor(
    mentor_id: int = Query(..., description="Mentor ID"),
    duration: int = Query(..., description="Duration in months (e.g. 1, 3, 6)"),
    session: Session = Depends(get_session)
):
    return MentorshipPlanService.fetch_selected_fields_by_mentor_and_duration(session, mentor_id, duration)