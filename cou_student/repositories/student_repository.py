from sqlmodel import Session, select
from fastapi import HTTPException
from cou_student.models.student import Student

def create_student(session: Session, student: Student) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def read_student(session: Session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def read_all_student(session: Session) -> list[Student]:
    return session.exec(select(Student)).all()

def update_student(session: Session, student_id: int, updated_data: dict) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updated_data.items():
        setattr(student, key, value)
    session.commit()
    session.refresh(student)
    return student

def delete_student(session: Session, student_id: int):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
