from typing import List, Optional
from sqlmodel import Session, select

from cou_user.models.skill import Skill
from cou_user.schemas.skill_schema import SkillCreate, SkillUpdate

class SkillRepository:
    def create(self, db: Session, *, obj_in: SkillCreate) -> Skill:
        db_obj = Skill(
            skill_name=obj_in.skill_name,
            description=obj_in.description,
            category_id=obj_in.category_id,
            subcategory_id=obj_in.subcategory_id,
            active=obj_in.active,
            created_by=obj_in.created_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Skill]:
        return db.exec(select(Skill).where(Skill.id == id)).first()

    def get_all(self, db: Session) -> List[Skill]:
        return db.exec(select(Skill)).all()

    def update(self, db: Session, *, db_obj: Skill, obj_in: SkillUpdate) -> Skill:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Skill:
        obj = db.get(Skill, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

skill_repository = SkillRepository() 