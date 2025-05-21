from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List, Optional, Dict
from cou_mentor.models.mentor import Mentor
from sqlalchemy import text
import base64

from sqlmodel import Session
from sqlalchemy.sql import text

class MentorRepository:
    @staticmethod
    def get_mentor_by_id(session: Session, mentor_id: int) -> Optional[Mentor]:
        """
        Retrieve a mentor by their ID.
        """
        return session.get(Mentor, mentor_id)

    @staticmethod
    def get_all_mentors(session: Session) -> List[Mentor]:
        """
        Retrieve all mentors.
        """
        return session.exec(select(Mentor)).all()

    @staticmethod
    def create_mentor(session: Session, mentor_data: dict) -> Mentor:
        """
        Create a new mentor.
        """
        mentor = Mentor(**mentor_data)
        session.add(mentor)
        session.commit()
        session.refresh(mentor)
        return mentor

    @staticmethod
    def update_mentor(session: Session, mentor_id: int, mentor_data: dict) -> Optional[Mentor]:
        """
        Update an existing mentor.
        """
        mentor = session.get(Mentor, mentor_id)
        if mentor:
            for key, value in mentor_data.items():
                setattr(mentor, key, value)
            session.commit()
            session.refresh(mentor)
        return mentor

    @staticmethod
    def delete_mentor(session: Session, mentor_id: int) -> bool:
        """
        Delete a mentor by their ID.
        """
        mentor = session.get(Mentor, mentor_id)
        if mentor:
            session.delete(mentor)
            session.commit()
            return True
        return False

    @staticmethod
    def get_mentors_by_expertise(session: Session, expertise: str) -> List[Mentor]:
        """
        Retrieve mentors by their expertise.
        """
        return session.exec(select(Mentor).where(Mentor.expertise == expertise)).all()

    @staticmethod
    def get_mentors_by_rating(session: Session, min_rating: float) -> List[Mentor]:
        """
        Retrieve mentors with a rating greater than or equal to the specified value.
        """
        return session.exec(select(Mentor).where(Mentor.rating >= min_rating)).all()

    @staticmethod
    def get_available_mentors(session: Session) -> List[Mentor]:
        """
        Retrieve all available mentors.
        """
        return session.exec(select(Mentor).where(Mentor.is_available == True)).all()

    @staticmethod
    def get_mentors_by_expertise(session: Session, expertise: str) -> List[Mentor]:
        """
        Retrieve mentors by their expertise.
        """
        return session.exec(select(Mentor).where(Mentor.expertise == expertise)).all()

    @staticmethod
    def get_mentors_by_rating(session: Session, min_rating: float) -> List[Mentor]:
        """
        Retrieve mentors with a rating greater than or equal to the specified value.
        """
        return session.exec(select(Mentor).where(Mentor.rating >= min_rating)).all()

    @staticmethod
    def get_available_mentors(session: Session) -> List[Mentor]:
        """
        Retrieve all available mentors.
        """
        return session.exec(select(Mentor).where(Mentor.is_available == True)).all()
    
    @staticmethod
    def get_all_mentors(session: Session) -> List[Mentor]:
        """
        Retrieve all mentors.
        """
        return session.exec(select(Mentor)).all()

    @staticmethod
    def get_filtered_mentors(
        session: Session,
        category_id: Optional[int] = None,
        region: Optional[str] = None,
        gender: Optional[str] = None,
        # Removed mentor_name parameter
        country_id: Optional[int] = None,
        language_id: Optional[int] = None,
        skill_id: Optional[int] = None,
        hourly_rate: Optional[float] = None,
        availability_day: Optional[str] = None,
    ) -> List[Dict]:
        query = """
            SELECT DISTINCT 
                u.display_name,
                u.image, 
                m.bio, 
                m.overall_experience, 
                m.availability_schedule, 
                m.additional_details, 
                m.avg_students_rating, 
                m.hourly_rate
            FROM 
                cou_user."user" u
            JOIN 
                cou_mentor.mentor m ON u.id = m.user_id
            LEFT JOIN 
                cou_course.course cr ON cr.mentor_id = m.user_id
            LEFT JOIN 
                cou_course.course_category cc ON cr.category_id = cc.id
            LEFT JOIN 
                cou_admin.country c ON u.country_id = c.id
            LEFT JOIN 
                cou_admin.language l ON cr.language_id = l.id
            LEFT JOIN 
                cou_user.user_skills us ON u.id = us.user_id
            LEFT JOIN 
                cou_user.skill s ON us.skill_id = s.id
            WHERE 
                u.active = true 
                AND m.active = true
        """

        # Apply dynamic filters
        if category_id:
            query += " AND cc.id = :category_id"
        if region:
            query += " AND u.region = :region"
        if gender:
            query += " AND u.gender = :gender"
        # Removed mentor_name condition
        if country_id:
            query += " AND c.id = :country_id"
        if language_id:
            query += " AND l.id = :language_id"
        if skill_id:
            query += " AND us.skill_id = :skill_id"
        if hourly_rate:
            query += " AND m.hourly_rate = :hourly_rate"
        if availability_day:
            query += " AND m.availability_schedule::jsonb ->> :availability_day IS NOT NULL"

        result = session.execute(
            text(query), 
            {
                "category_id": category_id,
                "region": region,
                "gender": gender,
                # Removed mentor_name from parameters
                "country_id": country_id,
                "language_id": language_id,
                "skill_id": skill_id,
                "hourly_rate": hourly_rate,
                "availability_day": availability_day
            }
        ).mappings().all()

        # Convert image (BYTEA) to Base64
        mentors = []
        for row in result:
            mentor = dict(row)
            if mentor.get("image"):
                # Convert bytea (memoryview) to Base64 string
                mentor["image"] = base64.b64encode(mentor["image"]).decode("utf-8")
                mentor["image"] = f"data:image/png;base64,{mentor['image']}"
            mentors.append(mentor)

        return mentors
   
    @staticmethod
    def get_filtered_mentors_by_names(
        session: Session,
        category: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        skill: Optional[str] = None,
        gender: Optional[str] = None,
        region: Optional[str] = None,
        budget: Optional[float] = None,
        availability_day: Optional[str] = None,
        mentor: Optional[str] = None
    ) -> List[Dict]:
        query = '''
        SELECT 
            u.display_name AS mentor_name,
            u.image AS mentor_image,
            m.bio,
            m.additional_details,
            m.overall_experience,
            m.avg_students_rating AS rating,
            m.hourly_rate AS budget,
            m.availability_schedule
        FROM 
            cou_user."user" u
        JOIN 
            cou_mentor.mentor m ON u.id = m.user_id
        LEFT JOIN 
            cou_course.course c ON c.mentor_id = m.user_id
        LEFT JOIN 
            cou_course.course_category cc ON c.category_id = cc.id
        LEFT JOIN 
            cou_admin.country cn ON u.country_id = cn.id
        LEFT JOIN 
            cou_admin.language l ON c.language_id = l.id
        LEFT JOIN 
            cou_user.user_skills us ON us.user_id = u.id
        LEFT JOIN 
            cou_user.skill s ON us.skill_id = s.id
        WHERE 
            u.active = true 
            AND m.active = true
            AND (:category IS NULL OR cc.name ILIKE '%' || :category || '%')
            AND (:country IS NULL OR cn.name ILIKE '%' || :country || '%')
            AND (:language IS NULL OR l.name ILIKE '%' || :language || '%')
            AND (:skill IS NULL OR s.skill_name ILIKE '%' || :skill || '%')
            AND (:gender IS NULL OR u.gender ILIKE '%' || :gender || '%')
            AND (:region IS NULL OR u.region ILIKE '%' || :region || '%')
            AND (:budget IS NULL OR m.hourly_rate <= :budget)
            AND (:availability_day IS NULL OR m.availability_schedule::text ILIKE '%' || :availability_day || '%')
            AND (:mentor IS NULL OR u.display_name ILIKE '%' || :mentor || '%')
        ORDER BY 
            u.display_name ASC;
        '''

        result = session.execute(
            text(query), {
                "category": category,
                "country": country,
                "language": language,
                "skill": skill,
                "gender": gender,
                "region": region,
                "budget": budget,
                "availability_day": availability_day,
                "mentor": mentor
            }
        ).mappings().all()

        mentors = []
        for row in result:
            mentor = dict(row)
            image_bytes = mentor.get("mentor_image")
            if image_bytes:
                try:
                    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                    mentor["mentor_image"] = f"data:image/png;base64,{encoded_image}"
                except Exception:
                    mentor["mentor_image"] = None
            else:
                mentor["mentor_image"] = None
            mentors.append(mentor)

        return mentors