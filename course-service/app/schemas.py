from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    fee: float = Field(..., ge=0)
    seats: int = Field(..., ge=0)

class CourseUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=120)
    fee: float | None = Field(None, ge=0)
    seats: int | None = Field(None, ge=0)

class CourseResponse(BaseModel):
    id: int
    name: str
    fee: float
    seats: int
    class Config:
        from_attributes = True
