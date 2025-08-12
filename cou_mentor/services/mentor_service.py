from typing import List, Optional,  Union,Dict
from sqlmodel import Session
from fastapi import HTTPException
from cou_mentor.repositories.mentor_repository import MentorRepository

from cou_mentor.models.mentor import Mentor
from sqlalchemy import text


class MentorService:
    @staticmethod
    def get_mentor(session, mentor_id: int) -> Mentor:
        """
        Retrieve a single mentor by ID.
        """
        mentor = MentorRepository.get_mentor_by_id(session, mentor_id)
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
        return mentor

    @staticmethod
    def get_all_mentors(session) -> List[Mentor]:
        """
        Retrieve all mentors.
        """
        mentors = MentorRepository.get_all_mentors(session)
        if not mentors:
            raise HTTPException(status_code=404, detail="No mentors available")
        return mentors

    @staticmethod
    def create_mentor(session, mentor_data: dict) -> Mentor:
        """
        Create a new mentor.
        """
        return MentorRepository.create_mentor(session, mentor_data)

    @staticmethod
    def update_mentor(session, mentor_id: int, mentor_data: dict) -> Mentor:
        """
        Update an existing mentor.
        """
        mentor = MentorRepository.update_mentor(session, mentor_id, mentor_data)
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")
        return mentor

    @staticmethod
    def delete_mentor(session, mentor_id: int) -> bool:
        """
        Delete a mentor by ID.
        """
        if not MentorRepository.delete_mentor(session, mentor_id):
            raise HTTPException(status_code=404, detail="Mentor not found")
        return True
    @staticmethod
    def search_mentors(session, expertise: Optional[str] = None, min_rating: Optional[float] = None) -> List[Mentor]:
        if expertise:
            return MentorRepository.get_mentors_by_expertise(session, expertise)
        elif min_rating:
            return MentorRepository.get_mentors_by_rating(session, min_rating)
        else:
            return MentorRepository.get_all_mentors(session)
        
    @staticmethod
    def get_all_mentors(session) -> Union[List[Mentor], str]:
        mentors = MentorRepository.get_all_mentors(session)
        if not mentors:
            return "No mentors available"
        return mentors
   
   
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
    ) -> List[dict]:
        return MentorRepository.get_filtered_mentors(
            session=session,
            subcategory_name=subcategory_name,
            country_name=country_name,
            language_name=language_name,
            overall_experience=overall_experience,
            offering_mentorship_for=offering_mentorship_for,
            companies=companies,
            avg_students_rating=avg_students_rating,
            open_for_inquires=open_for_inquires,
        )

    @staticmethod
    def get_mentor_profile_summary(user_id: int, session: Session):
        data = MentorRepository.fetch_mentor_profile_summary(user_id, session)
        if not data:
            raise HTTPException(status_code=404, detail="Mentor not found")
        return data
    @staticmethod
    def search_mentors(
        session: Session,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        skill: Optional[str] = None,
    ) -> List[dict]:
        return MentorRepository.search_mentors(
            session=session,
            name=name,
            domain=domain,
            skill=skill,
        )
        