from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from sqlalchemy.sql import select
from cou_course.models.course import Course
from cou_user.models.userCourse import UserCourse
from cou_user.schemas.userCourse_schema import UserCourseCreate, UserCourseRead, UserCourseDetailRead
# from cou_user.repositories.userCourse_repository import UserCourseRepository
from common.database import get_session
from cou_user.repositories.userCourse_repository import (
    create_usercourse,
    get_usercourse,
    list_usercourses,
    update_usercourse,
    delete_usercourse,
)
from cou_course.repositories.course_repository import CourseRepository
from datetime import datetime, timezone


router = APIRouter(
    prefix="/usercourse",
    tags=["UserCourse"]
)

@router.post("/", response_model=UserCourseRead)
def create_userCourse(usercourse: UserCourseCreate, session: Session = Depends(get_session)):
    db_usercourse = UserCourse.from_orm(usercourse)
    print("db_usercourse", db_usercourse)
    usercourse = create_usercourse(session, db_usercourse)
    return usercourse       

@router.get("/{usercourse_id}", response_model=UserCourseRead)
def read_usercourse(usercourse_id: int, session: Session = Depends(get_session)):
    repo = get_usercourse(session)
    usercourse = repo.get_usercourse(usercourse_id)
    if not usercourse:
        raise HTTPException(status_code=404, detail="UserCourse not found")
    return usercourse

@router.get("/", response_model=list[UserCourseDetailRead])
def list_usercourses_route(user_id: int, session: Session = Depends(get_session)):
    statement = (
        select(UserCourse, Course)
        .join(Course, Course.id == UserCourse.course_id)
        .where(UserCourse.user_id == user_id)
    )
    results = session.exec(statement).all()
    
    # Combine UserCourse and Course data
    user_course_details = [
        UserCourseDetailRead(
            id=usercourse.id,
            user_id=usercourse.user_id,
            course_id=usercourse.course_id,
            transaction_id=usercourse.transaction_id,
            cart_date=usercourse.cart_date,
            is_enrolled=usercourse.is_enrolled,
            enrollment_date=usercourse.enrollment_date,
            course_completion_status=usercourse.course_completion_status,
            created_at=usercourse.created_at,
            updated_at=usercourse.updated_at,
            created_by=usercourse.created_by,
            updated_by=usercourse.updated_by,
            active=usercourse.active,
            course_title=course.title,
            course_description=course.description,
            course_category_id=course.category_id,
            course_subcategory_id=course.subcategory_id,
            course_type_id=course.course_type_id,
            course_sells_type_id=course.sells_type_id,
            course_mentor_id=course.mentor_id,
            course_language_id=course.language_id,
            course_created_at=course.created_at,
            course_updated_at=course.updated_at,
            course_is_flagship=course.is_flagship,
            course_active=course.active,
            course_price=course.price
        )
        for usercourse, course in results
    ]
    
    return user_course_details

@router.put("/{usercourse_id}", response_model=UserCourseRead)
def update_usercourse(usercourse_id: int, usercourse: UserCourseCreate, session: Session = Depends(get_session)):
    repo = UserCourseRepository(session)
    usercourse_data = usercourse.dict(exclude_unset=True)
    return repo.update_usercourse(usercourse_id, usercourse_data)

@router.delete("/")
def delete_userCourse(user_id: int, course_id: int, session: Session = Depends(get_session)):
    status = delete_usercourse(session, user_id, course_id)
    return {"ok": status}

@router.post("/enroll", response_model=UserCourseRead)
def enroll_in_free_course(user_id: int, course_id: int, session: Session = Depends(get_session)):
    # Check if the course is free
    course = CourseRepository.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.price > 0:
        raise HTTPException(status_code=400, detail="Course is not free")

    # Check if the user is already enrolled
    existing_enrollment = get_usercourse(session, user_id, course_id)
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User is already enrolled in this course")

    # Enroll the user
    usercourse = UserCourse(
        user_id=user_id,
        course_id=course_id,
        is_enrolled=True,
        enrollment_date=datetime.now(timezone.utc)
    )
    session.add(usercourse)
    session.commit()
    session.refresh(usercourse)
    return usercourse
