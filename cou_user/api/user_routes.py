from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from common.database import get_session
from cou_user.models.user import User
from cou_user.schemas.user_schema import UserCreate, UserRead, UserUpdate
from cou_user.repositories.user_repository import (
    create_user,
    read_user,
    read_all_users,
    update_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserRead, summary="Create a new user")
def add_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.dict())
    return create_user(session, db_user)

@router.get("/{user_id}", response_model=UserRead, summary="Get user details by ID")
def get_user(user_id: int, session: Session = Depends(get_session)):
    return read_user(session, user_id)

@router.get("/", response_model=List[UserRead], summary="Get all users")
def get_all_users(session: Session = Depends(get_session)):
    return read_all_users(session)

@router.put("/{user_id}", response_model=UserRead, summary="Update user details")
def modify_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    return update_user(session, user_id, user_update.dict(exclude_unset=True))

@router.delete("/{user_id}", summary="Delete a user")
def remove_user(user_id: int, session: Session = Depends(get_session)):
    delete_user(session, user_id)
    return {"message": f"User with ID {user_id} has been deleted successfully."}