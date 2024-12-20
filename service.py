from fastapi import Depends,HTTPException
from models import User,Student
from schema import *
from sqlalchemy.orm import Session
from exceptions import UserNotFoundException
import bcrypt
from jwt import get_current_user


def get_user(db:Session, current_user=Depends(get_current_user)):
    return current_user

def create_new_user(data:CreateNewUser,db:Session):
    hashed_password=bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user=User(username=data.username,password=hashed_password.decode("utf-8"),role = data.role,is_deleted = False)
    if data.role != "admin" and data.role != "lecturer":
        raise HTTPException #yalniz admin ve mellim rollu istifadeci yaratmaq olar
    user=db.query(User).filter(User.username == new_user.username, User.is_deleted == False).first()
    if user:
        raise HTTPException #istifadeci movcuddur
    user1=db.query(User).filter(User.username == new_user.username, User.is_deleted == True).first()
    if user1:
        user1.username = data.username
        user1.password = hashed_password.decode("utf-8")
        user1.role = data.role
        user1.is_deleted = False
        db.commit()
        return {"msg":"new user is created"}
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"new user is created"}
        
def delete_user_from_db(data:DeleteUserSchema,db:Session,current_user=Depends(get_current_user)):
    current_user_in_db = db.query(User).filter(User.username==current_user['username']).first()
    if current_user_in_db.role != "admin":
        raise HTTPException(status_code=401,detail="permission denied")
    user_in_db = db.query(User).filter(User.username==data.username).first()
    if user_in_db.role != "lecturer":
        raise HTTPException #yalniz muellimleri silmek olar
    if user_in_db.is_deleted == True:
        raise HTTPException #artiq silinib
    user_in_db.is_deleted == True
    db.commit()
    db.refresh(user_in_db)
    message = f"{user_in_db.username} lecturer is deleted successfully"
    return message

def get_list_students(db:Session, current_user=Depends(get_current_user)):
    current_user_in_db = db.query(User).filter(User.username==current_user['username']).first()
    if current_user_in_db.role != "admin":
        raise HTTPException(status_code=401,detail="permission denied")
    students_list = []
    students = db.query(Student)
    for student in students:
        if student.is_deleted != False:
            pass
        student_dict = {
            "student_name":student.username,
            "student_surname":student.surname
            }
        students_list.append(student_dict)
    return students_list
