import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Student
from ..schemas import StudentCreate, StudentResponse, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])
COURSE_URL = "http://course-service:8002"

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(f"{COURSE_URL}/courses/{student_in.course_id}")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Course Service unavailable")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Course not found")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Course Service error")
    course = response.json()
    if course["seats"] <= 0:
        raise HTTPException(status_code=409, detail="No seats available")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            reserve = await client.post(f"{COURSE_URL}/courses/{student_in.course_id}/reserve")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Course Service unavailable")
    if reserve.status_code != 200:
        raise HTTPException(status_code=409, detail="Course seat reservation failed")
    student = Student(name=student_in.name, email=student_in.email, course_id=student_in.course_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student_in.name is not None:
        student.name = student_in.name
    if student_in.status is not None:
        student.status = student_in.status
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
