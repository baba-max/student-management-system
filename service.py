from fastapi import Depends
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