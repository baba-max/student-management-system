from fastapi import APIRouter,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *
from jwt import get_current_user

course_router = APIRouter()

@course_router.get("/courses")
def get_list_of_all_courses(db=Depends(get_db), current_user=Depends(get_current_user)):
    message = get_list_courses(db=db,current_user=current_user)
    return {"list of all active courses":message}

@course_router.post("/course")
def create_new_course(item:CreateCourseSchema,db=Depends(get_db),current_user=Depends(get_current_user)):
    message = create_course(data=item,db=db,current_user=current_user)
    return message