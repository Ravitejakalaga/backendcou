from typing import List, Union, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from cou_mentor.repositories.mentor_repository import MentorRepository
from cou_mentor.services.mentor_service import MentorService
from cou_mentor.models.mentor import Mentor
from cou_mentor.schemas.mentor_schema import MentorCreate, MentorUpdate, MentorRead
from common.database import get_session
from sqlalchemy import text

router = APIRouter(
    prefix="/mentors",
    tags=["Mentors"]
)

@router.get("/mentors/filtered", summary="Get mentors by dynamic filters")
def get_filtered_mentors(
    category_id: Optional[int] = Query(None, description="Category ID"),
    region: Optional[str] = Query(None, description="Region"),
    gender: Optional[str] = Query(None, description="Gender"),
    # mentor_name: Optional[str] = Query(None, description="Mentor Name"),  # Kept in route definition
    country_id: Optional[int] = Query(None, description="Country ID"),
    language_id: Optional[int] = Query(None, description="Language ID"),
    skill_id: Optional[int] = Query(None, description="Skill ID"),
    hourly_rate: Optional[float] = Query(None, description="Hourly Rate"),
    availability_day: Optional[str] = Query(None, description="Availability Day"),
    session: Session = Depends(get_session)
) -> List[Dict]:
    """
    Retrieve mentors based on dynamic filters.
    """
    mentors = MentorService.get_filtered_mentors(
        session,
        category_id=category_id,
        region=region,
        gender=gender,
        # mentor_name parameter removed
        country_id=country_id,
        language_id=language_id,
        skill_id=skill_id,
        hourly_rate=hourly_rate,
        availability_day=availability_day
    )
    
    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found for given filters")
    
    return mentors
# ✅ Get all Mentors
@router.get("/", response_model=Union[List[Mentor], str], summary="Get all mentors")
def get_all_mentors(session: Session = Depends(get_session)):
    return MentorService.get_all_mentors(session)


# ✅ Get Mentor by ID
@router.get("/{mentor_id}", response_model=MentorRead, summary="Get mentor by ID")
def get_mentor(mentor_id: int, session: Session = Depends(get_session)):
    mentor = MentorRepository.get_mentor_by_id(session, mentor_id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor


# ✅ Create Mentor
@router.post("/", response_model=MentorRead, summary="Create a new mentor")
def create_mentor(mentor: MentorCreate, session: Session = Depends(get_session)):
    return MentorRepository.create_mentor(session, mentor.dict())


# ✅ Update Mentor
@router.put("/{mentor_id}", response_model=MentorRead, summary="Update mentor by ID")
def update_mentor(mentor_id: int, mentor: MentorUpdate, session: Session = Depends(get_session)):
    updated_mentor = MentorRepository.update_mentor(session, mentor_id, mentor.dict(exclude_unset=True))
    if not updated_mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return updated_mentor


# ✅ Delete Mentor
@router.delete("/{mentor_id}", summary="Delete mentor by ID")
def delete_mentor(mentor_id: int, session: Session = Depends(get_session)):
    if not MentorRepository.delete_mentor(session, mentor_id):
        raise HTTPException(status_code=404, detail="Mentor not found")
    return {"message": "Mentor deleted successfully"}


# ✅ Get Mentor Mentee Details
@router.get("/{mentor_id}/mentee-details", summary="Get mentor's mentee and course details")
def get_mentor_mentee_details(mentor_id: int, session: Session = Depends(get_session)):
    query = text("""
        SELECT 
            u.display_name AS mentor_name,
            c.name AS country_name,
            COUNT(DISTINCT uc.user_id) AS mentee_count, 
            COUNT(DISTINCT co.id) AS course_count
        FROM cou_user."user" u
        LEFT JOIN cou_admin.country c ON u.country_id = c.id
        LEFT JOIN cou_course.course co ON co.mentor_id = u.id
        LEFT JOIN cou_user.user_course uc ON co.id = uc.course_id
        WHERE u.id = :mentor_id
        GROUP BY u.display_name, c.name
    """)
    result = session.execute(query, {"mentor_id": mentor_id}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Mentor not found or no data available")
    
    # Access result using index positions
    return {
        "mentor_id": mentor_id,
        "mentor_name": result[0],  # mentor_name
        "country_name": result[1], # country_name
        "mentee_count": result[2], # mentee_count
        "course_count": result[3]  # course_count
    }


# ✅ Get Mentor Courses
@router.get("/{mentor_id}/courses", summary="Get mentor's courses")
def get_mentor_courses(mentor_id: int, session: Session = Depends(get_session)):
    query = text("""
        SELECT 
            c.title AS course_name,
            c.description AS course_description,
            c.price AS course_price,
            u.display_name AS mentor_name
        FROM cou_course.course c
        JOIN cou_user."user" u ON c.mentor_id = u.id
        WHERE c.mentor_id = :mentor_id AND c.active = true
    """)
    
    results = session.execute(query, {"mentor_id": mentor_id}).fetchall()
    if not results:
        raise HTTPException(status_code=404, detail="No courses found for this mentor")
    
    return {
        "mentor_id": mentor_id,
        "courses": [dict(row._mapping) for row in results]
    }


@router.get("/mentors/filt", summary="Get mentors by dynamic filters")
def get_filtered_mentors(
    category: Optional[str] = Query(None, description="Category"),
    country: Optional[str] = Query(None, description="Country"),
    language: Optional[str] = Query(None, description="Language"),
    skill: Optional[str] = Query(None, description="Skill"),
    gender: Optional[str] = Query(None, description="Gender"),
    region: Optional[str] = Query(None, description="Region"),
    budget: Optional[float] = Query(None, description="Maximum Budget"),
    availability_day: Optional[str] = Query(None, description="Availability Day"),
    mentor: Optional[str] = Query(None, description="Mentor"),
    session: Session = Depends(get_session)
) -> List[Dict]:
    mentors = MentorRepository.get_filtered_mentors_by_names(
        session=session,
        category=category,
        country=country,
        language=language,
        skill=skill,
        gender=gender,
        region=region,
        budget=budget,
        availability_day=availability_day,
        mentor=mentor
    )

    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found matching the criteria.")

    return mentors