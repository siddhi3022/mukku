from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fee = Column(Float, nullable=False)
    seats = Column(Integer, nullable=False)
