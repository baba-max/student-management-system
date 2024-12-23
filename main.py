from fastapi import FastAPI
from db import get_db
from sqlalchemy.orm import Session
from user_router import user_router
from student_router import student_router
from course import course_router
from login import login_router

app = FastAPI(title="Individual Work", version="0.1.0")

@app.get("/")
def health_check():
    return {"msg":"hello"}

app.include_router(login_router)
app.include_router(user_router)
app.include_router(student_router)
app.include_router(course_router)