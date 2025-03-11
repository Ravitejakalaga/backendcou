from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from cou_course.models.course import Course
from cou_course.schemas.course_schema import CourseCreate, CourseRead, CourseUpdate
from cou_course.repositories.course_repository import CourseRepository
from common.database import get_session
from typing import Optional, List
from fastapi import Query
import logging
router = APIRouter()

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post("/", response_model=CourseRead)
def create_course(course: CourseCreate, session: Session = Depends(get_session)):
    course_model = Course(**course.dict())
    return CourseRepository.create_course(session, course_model)

@router.get("/filter", response_model=List[CourseRead])
def get_courses(
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(None),
    subcategory_id: Optional[int] = Query(None),
    course_type_id: Optional[int] = Query(None),
    sells_type_id: Optional[int] = Query(None),
    language_id: Optional[int] = Query(None),
    mentor_id: Optional[int] = Query(None),
    is_flagship: Optional[bool] = Query(None),
    active: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_ratings: Optional[float] = Query(None),
    max_ratings: Optional[float] = Query(None),
):
    """
    Get all courses or filter them by optional query parameters.
    Examples:
      - GET /courses (no filters => returns all courses)
      - GET /courses?category_id=2
      - GET /courses?language_id=3&active=true
      - GET /courses?min_price=0&max_price=100
      - GET /courses?min_ratings=4
      - GET /courses?subcategory_id=5&course_type_id=1
    """
    logging.debug("hey")
    courses = CourseRepository.filter_courses(
        session=session,
        category_id=category_id,
        subcategory_id=subcategory_id,
        course_type_id=course_type_id,
        sells_type_id=sells_type_id,
        language_id=language_id,
        mentor_id=mentor_id,
        is_flagship=is_flagship,
        active=active,
        min_price=min_price,
        max_price=max_price,
        min_ratings=min_ratings,
        max_ratings=max_ratings
    )
    return courses

@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, session: Session = Depends(get_session)):
    course = CourseRepository.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=List[CourseRead])
def get_all_courses(session: Session = Depends(get_session)):
    return CourseRepository.get_all_courses(session)

@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course_update: CourseUpdate, session: Session = Depends(get_session)):
    updates = course_update.dict(exclude_unset=True)
    updated_course = CourseRepository.update_course(session, course_id, updates)
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated_course

@router.delete("/{course_id}", response_model=dict)
def delete_course(course_id: int, session: Session = Depends(get_session)):
    if not CourseRepository.delete_course(session, course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}


