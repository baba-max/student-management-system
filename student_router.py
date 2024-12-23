from fastapi import APIRouter,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *
from jwt import get_current_user

student_router = APIRouter()

@student_router.get("/students")
def get_list_of_students(db=Depends(get_db), current_user=Depends(get_current_user)):
    message = get_list_students(db=db,current_user=current_user)
    return {"list of all active students":message}

@student_router.post("/student")
def create_new_student(item: CreateStudentSchema, db=Depends(get_db),current_user=Depends(get_current_user)):
    new_user = create_student(data=item,db=db,current_user=current_user)
    return {"msg":"new student is created successfully"}

@student_router.get("/student/ID")
def get_student_data(id:int,db=Depends(get_db),current_user=Depends(get_current_user)):
    result = get_student_by_id(id=id,db=db,current_user=current_user)
    return {"msg":result}