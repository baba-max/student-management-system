from fastapi import Depends,HTTPException
from models import User
from schema import *
from sqlalchemy.orm import Session
from exceptions import UserNotFoundException
import bcrypt
from jwt import get_current_user
from login import read_users_me


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def get_user(db:Session, current_user=Depends(get_current_user)):
    return current_user

def create_new_user(item:CreateNewUser,db:Session):
    new_user = User(username=item.username, password=hash_password(item.password),role=item.role,is_deleted=False)
    if new_user.role!="admin" and new_user.role!="lecturer":
        message = "You can create only lecturer or admin user"
        return message
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    message = f"New {new_user.role} is created successfully"
    return message
        
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