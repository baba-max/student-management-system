from fastapi import APIRouter, Depends
from jwt import get_current_user
from sqlalchemy.orm import Session
from db import get_db
from schema import *
from service import *

grade_router = APIRouter()


@grade_router.get("/grade/{student_id}")
def get_grade_by_id(student_id, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    message = get_grade_by_id_from_db(student_id=student_id, current_user=current_user, db=db)
    return {"list of all active subjects for lecturer":message}
