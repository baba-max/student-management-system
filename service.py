from fastapi import Depends,HTTPException
from models import User,Student,Registration,Course
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
        raise HTTPException #istifadeci mov
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
    user_in_db.is_deleted = True
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


def create_student(data:CreateStudentSchema, db:Session, current_user=Depends(get_current_user)):
    current_user_in_db = db.query(User).filter(User.username==current_user['username']).first()
    if current_user_in_db.role != "admin":
        raise HTTPException(status_code=401,detail="permission denied")
    new_student=Student(username=data.username,surname=data.surname,fin = data.fin,date=data.date,is_deleted = False)
    student=db.query(Student).filter(Student.fin == new_student.fin, Student.is_deleted == False).first()
    if student:
        raise HTTPException #student movcuddur
    student1=db.query(Student).filter(Student.fin == new_student.fin, Student.is_deleted == True).first()
    if student1:
        student1.username = data.username
        student1.surname = data.surname
        student1.role = data.fin
        student1.is_deleted = False
        db.commit()
        return {"msg":"new student is created"}
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"msg":"new student is created"}


def get_student_by_id(id:int, db:Session, current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student = db.query(Student).filter(Student.id == id, Student.is_deleted == False).first()
    if not student:
        raise HTTPException #student tapilmir
    register_course = db.query(Registration).filter(Registration.student_name == student.username, Registration.is_deleted == False).all()
    if not register_course:
        result1 = "His student has not registered for any course"
        a = student.username
        for i in student.username:
            if i.isdigit():
                b = a.replace(i, "")
        
        return {"username":b,"surname":student.surname,"date":student.date,"course_name":result1}
        
    else:
        result = ", ".join(i.course_name for i in register_course)
        end = "".join([char for char in result if not char.isdigit()])
        for i in register_course:
            name = ''.join([char for char in i.name if not char.isdigit()])
        return {"name":name,"surname":student.surname,"birthdate":student.date,"course_name":end}
    
    
    
#course router

def get_list_courses(db:Session, current_user=Depends(get_current_user)):
    current_user_in_db = db.query(User).filter(User.username==current_user['username']).first()
    if current_user_in_db.role != "admin":
        raise HTTPException(status_code=401,detail="permission denied")
    list_of_all_courses =[]
    courses = db.query(Course)
    for course in courses:
        if course.is_deleted != False:
            pass
        course_dict = {
            "subject_name":course.subject,
            }
        list_of_all_courses.append(course_dict)
    return list_of_all_courses    


def create_course(data:CreateCourseSchema,db:Session,current_user=Depends(get_current_user)):
    current_user_in_db = db.query(User).filter(User.username==current_user['username']).first()
    if current_user_in_db.role != "admin":
        raise HTTPException(status_code=401,detail="permission denied")
    teacher = db.query(User).filter(User.id == data.teacher_id, User.role == "lecturer", User.is_deleted == False).first()
    if not teacher:
        raise HTTPException #muellim yoxdur
    
    new_course = Course(teacher_id=data.teacher_id,subject=data.subject,description=data.description,is_deleted=False)
    course = db.query(Course).filter(Course.is_deleted==False).first()
    if course:
        raise HTTPException #kurs movcuddur
    deleted_course = db.query(Course).filter(Course.is_deleted==True).first()
    if deleted_course:
        deleted_course.teacher_id = data.teacher_id
        deleted_course.subject = data.subject
        deleted_course.description = data.description
        deleted_course.is_deleted = False
        db.commit()
        return {"msg": "new course is created successfully"}
    db.add(new_course)
    db.commit()
    db.refresh(new_course)  
    return {"msg": "new course is created successfully"}

