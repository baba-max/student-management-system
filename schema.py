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