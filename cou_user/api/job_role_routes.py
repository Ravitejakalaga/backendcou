from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.database import get_session
from cou_user.repositories.job_role_repository import job_role_repository
from cou_user.schemas.job_role_schema import JobRoleCreate, JobRoleUpdate, JobRoleInDB

router = APIRouter(
    prefix="/job-roles",
    tags=["Job Roles"]
)

@router.post("/", response_model=JobRoleInDB, summary="Create a new job role")
def create_job_role(
    *,
    db: Session = Depends(get_session),
    job_role_in: JobRoleCreate,
) -> JobRoleInDB:
    return job_role_repository.create(db=db, obj_in=job_role_in)

@router.get("/", response_model=List[JobRoleInDB], summary="Get all job roles")
def read_job_roles(
    db: Session = Depends(get_session),
) -> List[JobRoleInDB]:
    return job_role_repository.get_all(db=db)

@router.get("/{job_role_id}", response_model=JobRoleInDB, summary="Get a job role by ID")
def read_job_role(
    *,
    db: Session = Depends(get_session),
    job_role_id: int,
) -> JobRoleInDB:
    job_role = job_role_repository.get(db=db, id=job_role_id)
    if not job_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return job_role

@router.put("/{job_role_id}", response_model=JobRoleInDB, summary="Update a job role")
def update_job_role(
    *,
    db: Session = Depends(get_session),
    job_role_id: int,
    job_role_in: JobRoleUpdate,
) -> JobRoleInDB:
    job_role = job_role_repository.get(db=db, id=job_role_id)
    if not job_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return job_role_repository.update(db=db, db_obj=job_role, obj_in=job_role_in)

@router.delete("/{job_role_id}", response_model=JobRoleInDB, summary="Delete a job role")
def delete_job_role(
    *,
    db: Session = Depends(get_session),
    job_role_id: int,
) -> JobRoleInDB:
    job_role = job_role_repository.delete(db=db, id=job_role_id)
    if not job_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return job_role 