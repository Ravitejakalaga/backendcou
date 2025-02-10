from sqlmodel import Session, select
from fastapi import HTTPException
from cou_user.models.user import User

def _convert_mobile_to_string(user: User) -> User:
    if user.mobile is not None:
        user.mobile = str(user.mobile)
    return user

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return _convert_mobile_to_string(user)

def read_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _convert_mobile_to_string(user)

def read_all_users(session: Session) -> list[User]:
    users = session.exec(select(User)).all()
    return [_convert_mobile_to_string(user) for user in users]

def update_user(session: Session, user_id: int, updated_data: dict) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_data.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return _convert_mobile_to_string(user)

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
