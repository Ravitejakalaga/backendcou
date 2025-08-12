from typing import List, Dict, Tuple,Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from cou_mentor.models.skill import UserSkills
from cou_mentor.models.mentor import Mentor
from cou_user.models.user import User
from sqlalchemy import text
import base64


from cou_mentor.schemas.request_schema import StudentRequest
from sqlmodel import select
from pydantic import BaseModel

class Skill(BaseModel):
    id: int
    description: str



class UserMentorSkillOut(BaseModel):
    id: int
    name: str
    cloudou_rating: float = 0
    skillmentor: List[dict]
    image: Optional[str] = None
    expertise: Optional[str] = None
    overall_experience: Optional[int] = None
    
    bio: Optional[str] = None
    avg_students_rating: Optional[float] = None
    comment: Optional[str] = None
    subcategory: Optional[str] = None
    offering_mentorship_for: Optional[str] = None
    language: Optional[str] = None
    designation: Optional[str] = None
    # For P

def categorize_skills(raw_skills: List[dict]) -> Dict[str, List[Skill]]:
    current, target, search = [], [], []
    for skill in raw_skills:
        s = Skill(id=int(skill["id"]), description=skill["description"])
        if "target" in skill.get("type", "").lower():
            target.append(s)
        elif "search" in skill.get("type", "").lower():
            search.append(s)
        else:
            current.append(s)
    return {"current_skills": current, "target_skills": target, "recent_search": search}

def combine_skills(current, target, search) -> List[Skill]:
    all_skills = {s.description.strip().lower(): s for s in (current + target + search)}
    return list(all_skills.values())

def calculate_skill_match(student_skills: List[Skill], mentor_skills: List[dict]) -> Tuple[int, float]:
    student_set = {s.description.strip().lower() for s in student_skills}
    mentor_set = {m["description"].strip().lower() for m in mentor_skills if "description" in m}
    matched = student_set & mentor_set
    score = len(matched)
    percent = (score / len(student_set)) * 100 if student_set else 0
    return score, round(percent, 2)

def get_student_skills(user_id: int, session: Session) -> Dict[str, List[Skill]]:
    stmt = select(UserSkills).where(UserSkills.user_id == user_id)
    result = session.exec(stmt).first()
    if not result:
        raise HTTPException(status_code=404, detail="User skills not found")

    all_skills = []
    for key in ["current_skills", "target_skills", "recent_search"]:
        value = getattr(result, key, {})
        if isinstance(value, dict) and "skills" in value:
            all_skills.extend(value["skills"])
        elif isinstance(value, list):
            all_skills.extend(value)

    if not all_skills:
        raise HTTPException(status_code=404, detail="No skills found")

    return categorize_skills(all_skills)




def get_user_mentor_skills(session: Session) -> List[UserMentorSkillOut]:
    query = text("""
        SELECT 
            u.id as user_id,
            u.display_name,
            u.image,
            u.languages_known,
            m.bio,
            m.cloudou_rating,
            m.avg_students_rating,
            m.offering_mentorship_for,
            m.designation,
            m.overall_experience,  -- ✅ Newly added field
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
    """)

    results = session.execute(query).mappings().all()
    mentors = []
    seen_ids = set()

    for row in results:
        user_id = row["user_id"]
        if user_id in seen_ids:
            continue
        seen_ids.add(user_id)

        # Extract skills
        skill_json = row["current_skills"]
        if isinstance(skill_json, dict) and "skills" in skill_json:
            current_skills = skill_json["skills"]
        elif isinstance(skill_json, list):
            current_skills = skill_json
        else:
            current_skills = []

        # Convert image to base64
        image_data = row["image"]
        image_url = None
        image_type = None
        if image_data:
            img_bytes = image_data.tobytes() if hasattr(image_data, "tobytes") else bytes(image_data)
            image_type = "application/octet-stream"
            if img_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                image_type = "image/png"
            elif img_bytes.startswith(b"\xff\xd8\xff"):
                image_type = "image/jpeg"
            elif img_bytes.startswith(b"GIF87a") or img_bytes.startswith(b"GIF89a"):
                image_type = "image/gif"
            elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
                image_type = "image/webp"

            base64_image = base64.b64encode(img_bytes).decode("utf-8")
            image_url = f"data:{image_type};base64,{base64_image}"

        mentors.append(UserMentorSkillOut(
            id=user_id,
            name=row["display_name"],
            cloudou_rating=row["cloudou_rating"] or 0,
            avg_students_rating=row["avg_students_rating"] or 0,
            overall_experience=row["overall_experience"] or 0,  # ✅ Added
            comment=row["comment"],
            skillmentor=current_skills,
            image=image_url,
            image_type=image_type,
            expertise=row["designation"],
            bio=row["bio"],
            offering_mentorship_for=row["offering_mentorship_for"],
            subcategory=row["subcategory"],
            language=row["languages_known"],
            designation=row["designation"]
        ))

    return mentors