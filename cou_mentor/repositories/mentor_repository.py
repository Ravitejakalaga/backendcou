from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List, Optional, Dict
from cou_mentor.models.mentor import Mentor

from sqlalchemy import text
import base64
import json

from sqlmodel import Session
from sqlalchemy.sql import text
import mimetypes





class MentorRepository:
 
    @staticmethod
    def fetch_mentor_profile_summary(user_id: int, session: Session):
        query = text("""
            SELECT 
                u.display_name,
                u.image,
                u.languages_known,
                m.bio,
                m.avg_students_rating,
                m.offering_mentorship_for,
                m.designation,
                m.overall_experience,
                us.current_skills,
                sr.comment,
                cs.name AS subcategory
            FROM cou_user."user" u
            JOIN cou_mentor.mentor m ON m.user_id = u.id
            LEFT JOIN cou_user.user_skills us ON us.user_id = u.id
            LEFT JOIN LATERAL (
                SELECT comment
                FROM cou_mentor.mentor_student_reviews
                WHERE mentor_id = m.id
                ORDER BY created_at DESC
                LIMIT 1
            ) sr ON true
            LEFT JOIN cou_course.course_subcategory cs ON cs.id = (m.additional_details->>'subcategory_id')::int
            WHERE u.id = :user_id
            LIMIT 1
        """)

        result = session.execute(query, {"user_id": user_id}).mappings().first()
        if not result:
            return None

        image_data = result["image"]
        image_url = None

        if image_data:
            img_bytes = image_data.tobytes() if hasattr(image_data, "tobytes") else bytes(image_data)
            mime_type = "application/octet-stream"

            if img_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                mime_type = "image/png"
            elif img_bytes.startswith(b"\xff\xd8\xff"):
                mime_type = "image/jpeg"
            elif img_bytes.startswith(b"GIF87a") or img_bytes.startswith(b"GIF89a"):
                mime_type = "image/gif"
            elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
                mime_type = "image/webp"

            base64_image = base64.b64encode(img_bytes).decode("utf-8")
            image_url = f"data:{mime_type};base64,{base64_image}"

        return {
            "display_name": result["display_name"],
            "image": image_url,
            "languages_known": result["languages_known"],
            "bio": result["bio"],
            "avg_students_rating": result["avg_students_rating"],
            "offering_mentorship_for": result["offering_mentorship_for"],
            "designation": result["designation"],
            "overall_experience": result["overall_experience"],
            "current_skills": result["current_skills"],
            "comment": result["comment"],
            "subcategory": result["subcategory"]
        }
        
    
   
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
        subcategory_name: Optional[str] = None,
        country_name: Optional[str] = None,
        language_name: Optional[str] = None,
        overall_experience: Optional[int] = None,
        offering_mentorship_for: Optional[str] = None,
        companies: Optional[str] = None,
        avg_students_rating: Optional[float] = None,
        open_for_inquires: Optional[bool] = None,
        match_any: bool = False
    ) -> List[dict]:
        base_filters = ["u.active = true", "m.active = true"]
        dynamic_filters = []
        params = {}

        if subcategory_name:
            dynamic_filters.append("cs.name ILIKE :subcategory_name")
            params["subcategory_name"] = f"%{subcategory_name}%"
        if country_name:
            dynamic_filters.append("coun.name ILIKE :country_name")
            params["country_name"] = f"%{country_name}%"
        if language_name:
            dynamic_filters.append("lang.name ILIKE :language_name")
            params["language_name"] = f"%{language_name}%"
        if overall_experience is not None:
            dynamic_filters.append("m.overall_experience >= :overall_experience")
            params["overall_experience"] = overall_experience
        if offering_mentorship_for:
            dynamic_filters.append("m.offering_mentorship_for ILIKE :offering_mentorship_for")
            params["offering_mentorship_for"] = f"%{offering_mentorship_for}%"
        if companies:
            dynamic_filters.append("m.companies ILIKE :companies")
            params["companies"] = f"%{companies}%"
        if avg_students_rating is not None:
            dynamic_filters.append("m.avg_students_rating >= :avg_students_rating")
            params["avg_students_rating"] = avg_students_rating
        if open_for_inquires is not None:
            dynamic_filters.append("m.open_for_inquires = :open_for_inquires")
            params["open_for_inquires"] = open_for_inquires

        where_clause = (
            " AND ".join(base_filters) + " AND (" + " OR ".join(dynamic_filters) + ")"
            if match_any and dynamic_filters
            else " AND ".join(base_filters + dynamic_filters)
        )

        query = f"""
        SELECT 
            u.display_name,
            u.image,
            m.designation,
            m.avg_students_rating,
            m.bio,
            m.overall_experience,
            lang.name AS language,
            m.offering_mentorship_for,
            m.open_for_inquires,
            us.current_skills,
            cs.name AS course_subcategory,
            ARRAY_AGG(DISTINCT msr.comment) FILTER (WHERE msr.comment IS NOT NULL) AS comments
        FROM cou_user."user" u
        JOIN cou_mentor.mentor m ON m.user_id = u.id
        LEFT JOIN cou_user.user_skills us ON us.user_id = u.id AND us.active = true
        LEFT JOIN cou_admin.country coun ON coun.id = u.country_id
        LEFT JOIN cou_admin.language lang ON lang.country_id = u.country_id
        LEFT JOIN cou_course.course c ON c.mentor_id = u.id AND c.active = true
        LEFT JOIN cou_course.course_subcategory cs ON cs.id = c.subcategory_id
        LEFT JOIN cou_mentor.mentor_student_reviews msr ON msr.mentor_id = m.id
        WHERE {where_clause}
        GROUP BY u.id, m.id, lang.name, us.current_skills, cs.name
        """

        result = session.exec(text(query).params(**params))
        rows = result.mappings().all()

        mentors = []
        for row in rows:
            mentor = dict(row)

            # Image handling
            image_data = mentor.get("image")
            if image_data:
                img_bytes = image_data.tobytes() if hasattr(image_data, "tobytes") else bytes(image_data)
                mime_type = "application/octet-stream"
                if img_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                    mime_type = "image/png"
                elif img_bytes.startswith(b"\xff\xd8\xff"):
                    mime_type = "image/jpeg"
                elif img_bytes.startswith(b"GIF87a") or img_bytes.startswith(b"GIF89a"):
                    mime_type = "image/gif"
                elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
                    mime_type = "image/webp"

                base64_image = base64.b64encode(img_bytes).decode("utf-8")
                mentor["image"] = f"data:{mime_type};base64,{base64_image}"
            else:
                mentor["image"] = None

            # Null safety
            mentor["comments"] = mentor.get("comments", []) or []
            mentor["current_skills"] = (
                mentor.get("current_skills", {}).get("skills", [])
                if isinstance(mentor.get("current_skills"), dict)
                else mentor.get("current_skills", [])
            )

            mentors.append(mentor)

        return mentors
    
 
  
    #
    # repositories/mentor_repository.py




    @staticmethod
    def search_mentors(
        session: Session,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        skill: Optional[dict] = None
    ) -> List[dict]:

        base_filters = ["u.active = true", "m.active = true"]
        dynamic_filters = []
        params = {}

        if name:
            dynamic_filters.append("u.display_name ILIKE :name")
            params["name"] = f"%{name}%"
        if domain:
            dynamic_filters.append("cs.name ILIKE :domain")
            params["domain"] = f"%{domain}%"
        if skill:
            dynamic_filters.append("""
                (
                    (jsonb_typeof(us.current_skills) = 'array' AND EXISTS (
                        SELECT 1 FROM jsonb_array_elements(us.current_skills) AS elem
                        WHERE elem->>'description' ILIKE :skill
                    ))
                    OR
                    (jsonb_typeof(us.current_skills) = 'object' AND EXISTS (
                        SELECT 1 FROM jsonb_array_elements(us.current_skills->'skills') AS elem
                        WHERE elem->>'description' ILIKE :skill
                    ))
                )
            """)
            params["skill"] = f"%{skill}%"

        where_clause = " AND ".join(base_filters + dynamic_filters)

        query = f"""
        SELECT 
            u.display_name AS name,
            u.image,
            m.designation,
            m.avg_students_rating,
            m.bio,
            m.overall_experience,
            us.current_skills AS skill,
            cs.name AS domain,
            lang.name AS language,
            ARRAY_AGG(DISTINCT msr.comment) FILTER (WHERE msr.comment IS NOT NULL) AS comments
        FROM cou_user."user" u
        JOIN cou_mentor.mentor m ON m.user_id = u.id
        LEFT JOIN cou_user.user_skills us ON us.user_id = u.id AND us.active = true
        LEFT JOIN cou_course.course c ON c.mentor_id = u.id AND c.active = true
        LEFT JOIN cou_course.course_subcategory cs ON cs.id = c.subcategory_id
        LEFT JOIN cou_mentor.mentor_student_reviews msr ON msr.mentor_id = m.id
        LEFT JOIN cou_admin.language lang ON lang.country_id = u.country_id
        WHERE {where_clause}
        GROUP BY u.id, m.id, us.current_skills, cs.name, lang.name
        """

        result = session.exec(text(query).params(**params))
        rows = result.mappings().all()

        mentors = []
        for row in rows:
            mentor = dict(row)

            # Convert image
            image_data = mentor.get("image")
            if image_data:
                img_bytes = image_data.tobytes() if hasattr(image_data, "tobytes") else bytes(image_data)
                mime_type = "application/octet-stream"
                if img_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                    mime_type = "image/png"
                elif img_bytes.startswith(b"\xff\xd8\xff"):
                    mime_type = "image/jpeg"
                elif img_bytes.startswith(b"GIF87a") or img_bytes.startswith(b"GIF89a"):
                    mime_type = "image/gif"
                elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
                    mime_type = "image/webp"
                base64_image = base64.b64encode(img_bytes).decode("utf-8")
                mentor["image"] = f"data:{mime_type};base64,{base64_image}"
            else:
                mentor["image"] = None

            # Parse skill JSON
            try:
                mentor["skill"] = json.loads(mentor["skill"]) if mentor.get("skill") else {}
            except Exception:
                mentor["skill"] = {}

            mentor["comments"] = mentor.get("comments", []) or []
            mentors.append(mentor)

        return mentors
       # ✅ NEW METHOD: Get availability schedule for a specific mentor

    @staticmethod

    def get_mentor_availability(session: Session, mentor_id: int) -> Optional[Dict]:

        """

        Retrieve a mentor's availability schedule by mentor ID.

        """

        mentor = session.get(Mentor, mentor_id)

        if not mentor:

            return None

        return {

            "mentor_id": mentor.id,

            "availability_schedule": mentor.availability_schedule

        }

 





