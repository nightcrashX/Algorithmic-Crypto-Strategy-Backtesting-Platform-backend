#user_schema.py
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name : str
    username : str
    contact : int
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserGet(BaseModel):
    name : str
    username : str
    contact : int
    email : EmailStr