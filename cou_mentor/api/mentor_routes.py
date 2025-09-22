# cou_mentor/api/mentor_routes.py
from typing import List, Union, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlmodel import Session
import base64
import os

from cou_mentor.repositories.mentor_repository import MentorRepository
from cou_mentor.services.mentor_service import MentorService
from cou_mentor.models.mentor import Mentor
from cou_mentor.schemas.mentor_schema import MentorCreate, MentorUpdate, MentorRead
from cou_mentor.schemas.request_schema import StudentRequest, userContext
from cou_mentor.utils.skill_matcher import (
    get_student_skills, get_user_mentor_skills, combine_skills,
    extract_keywords, get_matching_subcategories, get_mentors_by_subcategory_ids
)
from cou_mentor.utils.crew_agent import mentor_profile_agent
from common.database import get_session

router = APIRouter(prefix="/mentors", tags=["Mentors"])

# ---- crewai: optional import + feature flag
CREWAI_AVAILABLE = False
try:
    from crewai import Task, Crew  # type: ignore
    CREWAI_AVAILABLE = True
except Exception:
    CREWAI_AVAILABLE = False

ENABLE_CREWAI = os.getenv("ENABLE_CREWAI", "false").lower() == "true"


@router.get("/profile-summary/{user_id}")
def get_profile_summary(user_id: int, session: Session = Depends(get_session)):
    return MentorService.get_mentor_profile_summary(user_id, session)


@router.post("/top-mentor/")
def match_mentor(request: StudentRequest, session: Session = Depends(get_session)):
    # Guard AI route if crewai not available/enabled
    if not (CREWAI_AVAILABLE and ENABLE_CREWAI):
        raise HTTPException(status_code=503, detail="AI feature not enabled on this deployment")

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
        f"""Name: {m.name}\nBio: {m.bio or 'N/A'}"""
        for m in filtered_mentors
    )

    task = Task(
        description=(
            "Student is looking for a mentor. Below are the top mentor profiles "
            f"based on skill match and rating.\n\n{profiles_text}\n\n"
            "Select the best 1 or 2 mentors and explain why."
        ),
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
                "overall_experience": m.overall_experience
            }
            for m in filtered_mentors
        ]
    }


@router.get("/{mentor_id}", summary="Get mentor by ID")
def get_mentor_by_mentorid(mentor_id: int, session: Session = Depends(get_session)):
    # NOTE: fix the reviews join to m.id (not u.id)
    sql = text("""
        SELECT 
            u.display_name,
            u.image, 
            u.id,
            m.bio, 
            m.expertise,
            m.overall_experience, 
            m.availability_schedule, 
            m.additional_details, 
            m.avg_students_rating, 
            m.hourly_rate,
            u.languages_known,
            m.cloudou_rating,
            m.mentor_about,
            u.region,

            array_agg(DISTINCT us.current_skills) AS skills,

            json_agg(DISTINCT jsonb_build_object(
                'company_name', usrexp.company_name,
                'start_date', usrexp.start_date,
                'end_date', usrexp.end_date,
                'job_role_name', jobrole.job_role_name
            )) AS experiences,

            array_agg(DISTINCT ued.institution_name) AS institutions,

            json_agg(DISTINCT jsonb_build_object(
                'student_id', msr.student_id,
                'rating', msr.rating,
                'comments', msr.comment,
                'student_display_name', stu.display_name,
                'student_image', stu.image
            )) AS reviews

        FROM cou_user."user" AS u
        JOIN cou_mentor.mentor AS m ON u.id = m.user_id
        LEFT JOIN cou_user.user_skills AS us ON u.id = us.user_id
        LEFT JOIN cou_user.user_experience AS usrexp ON u.id = usrexp.user_id
        LEFT JOIN cou_user.job_role AS jobrole ON jobrole.id = usrexp.job_role_id
        LEFT JOIN cou_user.user_education AS ued ON u.id = ued.user_id
        LEFT JOIN cou_mentor.mentor_student_reviews AS msr ON m.id = msr.mentor_id
        LEFT JOIN cou_user."user" AS stu ON msr.student_id = stu.id

        WHERE u.active = true AND m.active = true AND u.id = :mentor_id
        GROUP BY 
            u.id, u.display_name, u.image, 
            m.bio, m.expertise, m.overall_experience, 
            m.availability_schedule, m.additional_details, 
            m.avg_students_rating, m.hourly_rate, 
            u.languages_known, m.cloudou_rating, 
            m.mentor_about, u.region;
    """)

    result = session.execute(sql, {"mentor_id": mentor_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Mentor not found")

    mentor = dict(result)

    # Convert mentor image bytes to data URL
    image_bytes = mentor.get("image")
    if image_bytes:
        image_bytes = bytes(image_bytes)
        mime_type = MentorRepository.detect_mime_type(image_bytes)
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        mentor["image"] = f"data:image/{mime_type};base64,{encoded}"
    else:
        mentor["image"] = None

    # NOTE: student images are inside the 'reviews' JSON, not top-level. If you need to
    # convert them as well, iterate mentor["reviews"] list and convert each 'student_image'.

    return mentor


@router.get("/", response_model=Union[List[Mentor], str], summary="Get all mentors")
def get_all_mentors(session: Session = Depends(get_session)):
    return MentorService.get_all_mentors(session)


@router.post("/", response_model=MentorRead, summary="Create a new mentor")
def create_mentor(mentor: MentorCreate, session: Session = Depends(get_session)):
    return MentorRepository.create_mentor(session, mentor.dict())


@router.put("/{mentor_id}", response_model=MentorRead, summary="Update mentor by ID")
def update_mentor(mentor_id: int, mentor: MentorUpdate, session: Session = Depends(get_session)):
    updated_mentor = MentorRepository.update_mentor(session, mentor_id, mentor.dict(exclude_unset=True))
    if not updated_mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return updated_mentor


@router.delete("/{mentor_id}", summary="Delete mentor by ID")
def delete_mentor(mentor_id: int, session: Session = Depends(get_session)):
    if not MentorRepository.delete_mentor(session, mentor_id):
        raise HTTPException(status_code=404, detail="Mentor not found")
    return {"message": "Mentor deleted successfully"}


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
    row = session.execute(query, {"mentor_id": mentor_id}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Mentor not found or no data available")

    return {
        "mentor_id": mentor_id,
        "mentor_name": row[0],
        "country_name": row[1],
        "mentee_count": row[2],
        "course_count": row[3]
    }


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
        "courses": [dict(r._mapping) for r in results]
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


@router.post("/top-mentor/user-challenge", summary="Match mentor based on user challenge")
def match_mentor_by_challenge(request: userContext, session: Session = Depends(get_session)):
    # Guard AI route if crewai not available/enabled
    if not (CREWAI_AVAILABLE and ENABLE_CREWAI):
        raise HTTPException(status_code=503, detail="AI feature not enabled on this deployment")

    if not request.challenges:
        raise HTTPException(status_code=400, detail="Challenge input is required.")

    challenge_keywords = extract_keywords(request.challenges)
    matched_subcategory_ids = get_matching_subcategories(challenge_keywords, session)
    mentors = get_mentors_by_subcategory_ids(matched_subcategory_ids, session)

    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found for the given challenge.")

    filtered_mentors = [m for m in mentors if m.avg_students_rating >= 3 and m.id != request.user_id]

    profiles_text = "\n\n".join(
        f"""Name: {m.name}\nBio: {m.bio or 'N/A'}\nDesignation: {m.designation or 'N/A'}"""
        for m in filtered_mentors
    )

    task = Task(
        description=(
            f'Student has the following challenge: "{request.challenges}".\n\n'
            f"The following mentor profiles are available:\n\n{profiles_text}\n\n"
            "Select the top 1 or 2 mentors and explain why they are the best match."
        ),
        expected_output="Name(s) of selected mentor(s) with justification.",
        agent=mentor_profile_agent
    )

    crew = Crew(agents=[mentor_profile_agent], tasks=[task], verbose=False)
    result = crew.kickoff()

    return {"summary": result, "top_matches": [m.dict() for m in filtered_mentors]}


@router.get("/mentor-availability/{mentor_id}", summary="Get mentor's availability schedule")
def get_mentor_availability(mentor_id: int, session: Session = Depends(get_session)):
    mentor = MentorRepository.get_mentor_by_id(session, mentor_id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    if not mentor.availability_schedule:
        raise HTTPException(status_code=404, detail="Availability schedule not found for this mentor")

    return {"mentor_id": mentor.id, "availability_schedule": mentor.availability_schedule}
