#security.py
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os
from fastapi import HTTPException , status , Depends
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from app.config.database import get_user_collection


load_dotenv(dotenv_path=".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGO =  os.getenv("ALGO")
EXPIRY_TIME = int(os.getenv("EXPIRY_TIME"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
) 
users = get_user_collection()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        hours=EXPIRY_TIME
    )
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGO
    )

    return encoded_jwt

def verify_access_token(token:str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=ALGO)

            return decode_token
        
        except JWTError :
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" Unauthorized or exprired token")
    
# token verify krega or user ko indentify krega 
def get_current_user(token: str ):

    payload = verify_access_token(token)

    user_id = payload["sub"]
    
    current_user = users.find_one({"_id":ObjectId(user_id)})
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return current_user





