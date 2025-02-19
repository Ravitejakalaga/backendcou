from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session
from common.database import get_session
from cou_student.models.student import Student
from cou_student.repositories.student_repository import (
    create_student,
    read_student,
    read_all_student,
    update_student,
    delete_student,
)

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)

@router.post("/", response_model=Student, summary="Create a new student")
def add_student(student: Student, session: Session = Depends(get_session)):
    return create_student(session, student)

@router.get("/{student_id}", response_model=Student, summary="Get student details by ID")
def get_student(student_id: int, session: Session = Depends(get_session)):
    return read_student(session, student_id)

@router.get("/", response_model=list[Student], summary="Get all students")
def get_all_students(session: Session = Depends(get_session)):
    return read_all_student(session)

@router.put("/{student_id}", response_model=Student, summary="Update student details")
def modify_student(student_id: int, updated_data: dict, session: Session = Depends(get_session)):
    return update_student(session, student_id, updated_data)

@router.delete("/{student_id}", summary="Delete a student")
def remove_student(student_id: int, session: Session = Depends(get_session)):
    delete_student(session, student_id)
    return {"message": f"Student with ID {student_id} has been deleted successfully."}