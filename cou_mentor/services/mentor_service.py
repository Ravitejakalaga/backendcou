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
        category_id: Optional[int] = None,
        region: Optional[str] = None,
        gender: Optional[str] = None,
       
        country_id: Optional[int] = None,
        language_id: Optional[int] = None,
        skill_id: Optional[int] = None,
        hourly_rate: Optional[float] = None,
        availability_day: Optional[str] = None,
    ) -> List[Dict]:
        return MentorRepository.get_filtered_mentors(
            session=session,
            category_id=category_id,
            region=region,
            gender=gender,
             country_id=country_id,
            language_id=language_id,
            skill_id=skill_id,
            hourly_rate=hourly_rate,
            availability_day=availability_day,
        )