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
