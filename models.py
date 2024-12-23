from sqlalchemy import Column,Integer,String,Float,Date,Boolean
from db import Base,engine
import datetime

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    role = Column(String)
    is_deleted = Column(Boolean)
    
class Student(Base):
    __tablename__="students"
    id = Column(Integer,primary_key=True)
    username = Column(String)
    surname = Column(String)
    fin = Column(String,unique=True)
    date = Column(Date)
    is_deleted = Column(Boolean)

class Course(Base):
    __tablename__="courses"
    id = Column(Integer,primary_key=True)
    teacher_id = Column(Integer)
    subject = Column(String)
    description = Column(String)
    is_deleted = Column(Boolean)
    
class Registration(Base):
    __tablename__="students course registration"
    id = Column(Integer,primary_key=True)
    course_name = Column(String)
    student_name = Column(String)
    final_note = Column(Float)
    is_deleted = Column(Boolean)
    
Base.metadata.create_all(bind=engine)