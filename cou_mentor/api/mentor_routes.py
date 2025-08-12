from typing import List, Union, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from cou_mentor.repositories.mentor_repository import MentorRepository
from cou_mentor.services.mentor_service import MentorService
from cou_mentor.models.mentor import Mentor



from cou_mentor.schemas.mentor_schema import MentorCreate, MentorUpdate, MentorRead
from common.database import get_session
from sqlalchemy import text
from crewai import Task, Crew
from cou_mentor.utils.skill_matcher import (
    get_student_skills, get_user_mentor_skills, combine_skills, calculate_skill_match
)
from cou_mentor.utils.crew_agent import mentor_profile_agent
from cou_mentor.schemas.request_schema import StudentRequest
from cou_user.schemas.user_schema import UserRead
import base64


router = APIRouter(
    prefix="/mentors",
    tags=["Mentors"]
    
    
)



@router.get("/profile-summary/{user_id}")
def get_profile_summary(user_id: int, session: Session = Depends(get_session)):
    return MentorService.get_mentor_profile_summary(user_id, session)

@router.post("/top-mentor/")
def match_mentor(request: StudentRequest, session: Session = Depends(get_session)):
    student_skills = get_student_skills(request.user_id, session)
    combined_skills = combine_skills(
        student_skills["current_skills"],
        student_skills["target_skills"],
        student_skills["recent_search"]
    )

    mentors = get_user_mentor_skills(session)
    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found")

    filtered_mentors = [
        mentor for mentor in mentors
        if mentor.id != request.user_id
        and mentor.avg_students_rating is not None and mentor.avg_students_rating >= 3
    ]

    profiles_text = "\n\n".join(
        f"""Name: {m.name}\nBio: {m.bio or 'N/A'}""" for m in filtered_mentors
    )

    task = Task(
        description=f"""Student is looking for a mentor. Below are the top mentor profiles based on skill match and rating.\n\n{profiles_text}\n\nSelect the best 1 or 2 mentors and explain why.""",
        expected_output="Name(s) of selected mentor(s) with short justification.",
        agent=mentor_profile_agent
    )

    crew = Crew(agents=[mentor_profile_agent], tasks=[task], verbose=False)
    result = crew.kickoff()

    return {
        "summary": result,
        "top_matches": [
            {
                "id": m.id,
                "name": m.name,
                "avg_students_rating": m.avg_students_rating,
                "comment": m.comment,
                "image": m.image,
                "bio": m.bio,
                "skills": m.skillmentor,
                "subcategory": m.subcategory,
                "offering_mentorship_for": m.offering_mentorship_for,
                "language": m.language,
                "designation": m.designation,
                "overall_experience": m.overall_experience  # ✅ included in output
            }
            for m in filtered_mentors
        ]
    }





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




@router.get("/top/filtered", summary="Get filtered mentors", response_model=List[dict])
def get_filtered_mentors(
    subcategory_name: Optional[str] = Query(None),
    country_name: Optional[str] = Query(None),
    language_name: Optional[str] = Query(None),
    overall_experience: Optional[int] = Query(None),
    offering_mentorship_for: Optional[str] = Query(None),
    companies: Optional[str] = Query(None),
    avg_students_rating: Optional[float] = Query(None),
    open_for_inquires: Optional[bool] = Query(None),
    session: Session = Depends(get_session),
):
    return MentorService.get_filtered_mentors(
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
    
@router.get("/mentors/search")
def search_mentors(
    name: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    skill: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    return MentorService.search_mentors(
        session=session,
        name=name,
        domain=domain,
        skill=skill,
    )
    


    
