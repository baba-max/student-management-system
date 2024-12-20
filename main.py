from fastapi import FastAPI, APIRouter
from user_router import user_router
from student_router import student_router

app = FastAPI()

app.include_router(user_router)
app.include_router(student_router)