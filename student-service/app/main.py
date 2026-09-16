from fastapi import FastAPI
from .database import Base, engine
from .routers import students

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Student Microservice", version="1.0.0")
app.include_router(students.router)

@app.get("/")
def health_check():
    return {"service": "Student Service", "status": "healthy", "port": 8001}
