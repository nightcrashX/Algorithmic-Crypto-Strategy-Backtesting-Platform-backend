#auth_service.py
from fastapi import HTTPException, status , Response, Request
from app.config.database import get_user_collection
from app.schemas.user_schema import UserRegister
from app.schemas.user_schema import UserLogin
from app.utils.security import hash_password, verify_password ,create_access_token
from dotenv import load_dotenv
import os
import time

load_dotenv(dotenv_path=".env")
SECRET_KEY =  os.getenv("SECRET_KEY")
ALGO = os.getenv("ALGO")

users = get_user_collection()

response = Response()

def get_user(body: UserRegister):
    try :
        existing_user = users.find_one({"email": body.email})
        if existing_user :
            return { existing_user}
       
        return {
                "status": "user get successfully",
            }

    except Exception as e:
        return {"error": str(e) }

def register_user(body: UserRegister):
    try :
        existing_user = users.find_one({"email": body.email})
        # existing_user = users.create_index("email",unique=True)
        if existing_user :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        else:
            user_data = body.model_dump()   # convert to dict
            # user_data["_id"] = str(user_data["_id"])

            user_data["password"] = hash_password(user_data["password"])

            users.insert_one(user_data)
        return {
                "status": "user register successfully",
                # "user": user_data
            }

    except Exception as e:
        return {"error": str(e) }
    
def login_user(body: UserLogin):
    try:
        start = time.perf_counter()

        existing_user = users.find_one({"email": body.email})
        if not existing_user:
            raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Email or Password"
                        )
        
        password_match = verify_password(
                body.password,
                existing_user["password"]
            )
        if not password_match:      
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Email or Password"
                )
        
        token_data = {
            "sub": str(existing_user["_id"]),
            "email": existing_user["email"]
        }

        access_token = create_access_token(token_data)     # token generate
        return access_token


    except Exception :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email or password")
        



    

    
