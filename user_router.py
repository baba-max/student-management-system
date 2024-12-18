from fastapi import APIRouter,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *
from login import read_users_me

user_router = APIRouter()

@user_router.get("/user")
def get_current_user(db=Depends(get_db), current_user=Depends(get_current_user)):
    message = get_user(db=db, current_user=current_user)
    return message
    