from typing import List, Optional
from sqlmodel import Session, select

from cou_user.models.job_role import JobRole
from cou_user.schemas.job_role_schema import JobRoleCreate, JobRoleUpdate

class JobRoleRepository:
    def create(self, db: Session, *, obj_in: JobRoleCreate) -> JobRole:
        db_obj = JobRole(
            job_role_name=obj_in.job_role_name,
            description=obj_in.description,
            category_id=obj_in.category_id,
            subcategory_id=obj_in.subcategory_id,
            active=obj_in.active,
            created_by=obj_in.created_by,
            updated_by=obj_in.created_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[JobRole]:
        return db.exec(select(JobRole).where(JobRole.id == id)).first()

    def get_all(self, db: Session) -> List[JobRole]:
        return db.exec(select(JobRole)).all()

    def update(self, db: Session, *, db_obj: JobRole, obj_in: JobRoleUpdate) -> JobRole:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> JobRole:
        obj = db.get(JobRole, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

job_role_repository = JobRoleRepository() 