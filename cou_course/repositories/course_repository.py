from typing import Optional, List
from sqlmodel import Session, select
from cou_course.models.course import Course
from cou_user.models.user import User
import logging

class CourseRepository:
    @staticmethod
    def create_course(session: Session, course: Course) -> Course:
        session.add(course)
        session.commit()
        session.refresh(course)
        return course

    @staticmethod
    def get_course_by_id(session: Session, course_id: int) -> Optional[Course]:
        statement = (
            select(Course)
            .join(User, Course.mentor_id == User.id)
            .where(Course.id == course_id)
        )
        return session.exec(statement).first()

    @staticmethod
    def get_all_courses(session: Session) -> List[Course]:
        statement = (
            select(Course)
            .join(User, Course.mentor_id == User.id)
            .where(User.is_instructor == True)
        )
        return session.exec(statement).all()

    @staticmethod
    def update_course(session: Session, course_id: int, updates: dict) -> Optional[Course]:
        course = session.get(Course, course_id)
        if course:
            for key, value in updates.items():
                setattr(course, key, value)
            session.commit()
            session.refresh(course)
        return course

    @staticmethod
    def delete_course(session: Session, course_id: int) -> bool:
        course = session.get(Course, course_id)
        if course:
            session.delete(course)
            session.commit()
            return True
        return False
    
    @staticmethod
    def get_courses_by_mentor(session: Session, mentor_id: int):
        statement = (
            select(Course)
            .join(User, Course.mentor_id == User.id)
            .where(Course.mentor_id == mentor_id)
        )
        return session.exec(statement).all()
    
    
    @staticmethod
    def filter_courses(
        session: Session,
        category_id: Optional[int] = None,
        subcategory_id: Optional[int] = None,
        course_type_id: Optional[int] = None,
        sells_type_id: Optional[int] = None,
        language_id: Optional[int] = None,
        mentor_id: Optional[int] = None,
        is_flagship: Optional[bool] = None,
        active: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_ratings: Optional[float] = None,
        max_ratings: Optional[float] = None
    ) -> List[Course]:
        """
        Dynamically filter courses based on provided optional parameters.
        If none are provided, it returns all courses.
        """
        logging.debug("Filter parameters: %s", {
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "course_type_id": course_type_id,
            "sells_type_id": sells_type_id,
            "language_id": language_id,
            "mentor_id": mentor_id,
            "is_flagship": is_flagship,
            "active": active,
            "min_price": min_price,
            "max_price": max_price,
            "min_ratings": min_ratings,
            "max_ratings": max_ratings
        })

        query = select(Course)

        # 1) Match exact column values
        if category_id is not None:
            query = query.where(Course.category_id == category_id)
        if subcategory_id is not None:
            query = query.where(Course.subcategory_id == subcategory_id)
        if course_type_id is not None:
            query = query.where(Course.course_type_id == course_type_id)
        if sells_type_id is not None:
            query = query.where(Course.sells_type_id == sells_type_id)
        if language_id is not None:
            query = query.where(Course.language_id == language_id)
        if mentor_id is not None:
            query = query.where(Course.mentor_id == mentor_id)

        # 2) Boolean flags
        if is_flagship is not None:
            query = query.where(Course.is_flagship == is_flagship)
        if active is not None:
            query = query.where(Course.active == active)

        # 3) Ranges for price
        if min_price is not None:
            query = query.where(Course.price >= min_price)
        if max_price is not None:
            query = query.where(Course.price <= max_price)

        # 4) Ranges for ratings
        if min_ratings is not None:
            query = query.where(Course.ratings >= min_ratings)
        if max_ratings is not None:
            query = query.where(Course.ratings <= max_ratings)

        print("Query" , query)
        results = session.exec(query)
        return results.all()