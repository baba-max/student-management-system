from sqlalchemy import Column,Integer,String,Float,Date
from db import Base,engine
import datetime

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    role = Column(String)
    is_deleted = False
    
class Student(Base):
    __tablename__="students"
    id = Column(Integer,primary_key=True)
    username = Column(String)
    surname = Column(String)
    fin = Column(String)
    date = Column(Date)
    is_deleted = False

class Course(Base):
    __tablename__="courses"
    id = Column(Integer,primary_key=True)
    subject = Column(String)
    description = Column(String)
    is_deleted = False
    
class Registration(Base):
    __tablename__="students course registration"
    id = Column(Integer,primary_key=True)
    course_name = Column(String)
    student_name = Column(String)
    final_note = Column(Float)
    is_deleted = False
    
Base.metadata.create_all(bind=engine)