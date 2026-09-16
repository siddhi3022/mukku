from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Course
from ..schemas import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    course = Course(name=course_in.name, fee=course_in.fee, seats=course_in.seats)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{course_id}/reserve", response_model=CourseResponse)
def reserve_seat(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.seats <= 0:
        raise HTTPException(status_code=409, detail="No seats available")
    course.seats -= 1
    db.commit()
    db.refresh(course)
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_in: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course_in.name is not None:
        course.name = course_in.name
    if course_in.fee is not None:
        course.fee = course_in.fee
    if course_in.seats is not None:
        course.seats = course_in.seats
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}
