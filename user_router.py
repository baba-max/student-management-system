from fastapi import FastAPI,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *

user_router = FastAPI()

@user_router.get("/user")
