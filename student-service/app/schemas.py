from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=120)
    course_id: int = Field(..., gt=0)

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    course_id: int
    status: str
    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    status: str | None = Field(None, min_length=1, max_length=30)
