from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.database import get_session
from cou_user.repositories.skill_repository import skill_repository
from cou_user.schemas.skill_schema import SkillCreate, SkillUpdate, SkillInDB

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post("/", response_model=SkillInDB, summary="Create a new skill")
def create_skill(
    *,
    db: Session = Depends(get_session),
    skill_in: SkillCreate,
) -> SkillInDB:
    return skill_repository.create(db=db, obj_in=skill_in)

@router.get("/", response_model=List[SkillInDB], summary="Get all skills")
def read_skills(
    db: Session = Depends(get_session),
) -> List[SkillInDB]:
    return skill_repository.get_all(db=db)

@router.get("/{skill_id}", response_model=SkillInDB, summary="Get a skill by ID")
def read_skill(
    *,
    db: Session = Depends(get_session),
    skill_id: int,
) -> SkillInDB:
    skill = skill_repository.get(db=db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.put("/{skill_id}", response_model=SkillInDB, summary="Update a skill")
def update_skill(
    *,
    db: Session = Depends(get_session),
    skill_id: int,
    skill_in: SkillUpdate,
) -> SkillInDB:
    skill = skill_repository.get(db=db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill_repository.update(db=db, db_obj=skill, obj_in=skill_in)

@router.delete("/{skill_id}", response_model=SkillInDB, summary="Delete a skill")
def delete_skill(
    *,
    db: Session = Depends(get_session),
    skill_id: int,
) -> SkillInDB:
    skill = skill_repository.delete(db=db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill 