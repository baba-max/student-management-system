from pydantic import BaseModel
from datetime import date

class CreateNewUser(BaseModel):
    username: str
    password: str
    role: str
    class Config:
        extra="forbid"
        
class DeleteUserSchema(BaseModel):
    username: str
    class Config:
        extra = "forbid"
        
class CreateStudentSchema(BaseModel):
    username: str
    surname: str
    fin: str
    date: date
    class Config:
        extra = "forbid"
        
class CreateCourseSchema(BaseModel):
    teacher_id: int
    subject: str
    description: str
    class Config:
        extra = "forbid"