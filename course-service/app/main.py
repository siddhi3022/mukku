from fastapi import FastAPI
from .database import Base, engine
from .routers import courses

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Course Microservice", version="1.0.0")
app.include_router(courses.router)

@app.get("/")
def health_check():
    return {"service": "Course Service", "status": "healthy", "port": 8002}
