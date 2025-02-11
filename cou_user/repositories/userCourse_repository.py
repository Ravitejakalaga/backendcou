from sqlmodel import Session, select
from fastapi import HTTPException
from cou_user.models.userCourse import UserCourse
from cou_course.models.course import Course


def create_usercourse(session: Session, usercourse: UserCourse) -> UserCourse:
    # Check if the usercourse already exists
    statement = select(UserCourse).where(
        (UserCourse.user_id == usercourse.user_id) & 
        (UserCourse.course_id == usercourse.course_id)
    )
    existing_usercourse = session.exec(statement).first()
    
    if existing_usercourse:
        raise HTTPException(status_code=400, detail="UserCourse already exists.")
    
    session.add(usercourse)
    session.commit()
    session.refresh(usercourse)
    return usercourse

def get_usercourse(session: Session, user_id: int, course_id: int) -> UserCourse:
    statement = select(UserCourse).where(
        (UserCourse.user_id == user_id) & 
        (UserCourse.course_id == course_id)
    )
    find_usercourse = session.exec(statement).first()
    print("statement is finneddd", find_usercourse)
    return find_usercourse

def list_usercourses(session: Session, user_id: int) -> list[Course]:
    statement = (
        select(Course)
        .join(UserCourse, Course.id == UserCourse.course_id)
        .where(UserCourse.user_id == user_id)
    )
    return session.exec(statement).all()

def update_usercourse(session: Session, usercourse_id: int, usercourse_data: dict) -> UserCourse:
    usercourse = get_usercourse(session, usercourse_id)
    for key, value in usercourse_data.items():
        setattr(usercourse, key, value)
    session.commit()
    session.refresh(usercourse)
    return usercourse

def delete_usercourse(session: Session, user_id: int, course_id: int):
    usercourse = get_usercourse(session, user_id, course_id)
    print("usercourse is finneddd", usercourse)
    session.delete(usercourse)
    session.commit()