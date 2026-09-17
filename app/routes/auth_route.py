#auth_route.py
from fastapi import APIRouter , status, Header , Depends, Response, Request , HTTPException
from fastapi.responses import JSONResponse
from app.schemas.user_schema import UserRegister
from app.schemas.user_schema import UserLogin
from app.schemas.user_schema import UserGet
from app.services.auth_service import register_user
from app.services.auth_service import get_user
from app.services.auth_service import login_user
from app.utils.security import get_current_user
import time



user_routes = APIRouter(prefix="/user")


@user_routes.post("/register", status_code=status.HTTP_201_CREATED)
def register(body:UserRegister):
    return register_user(body)

        
@user_routes.post("/login")
def login(body: UserLogin):
    
    token = login_user(body)

    response = JSONResponse(
        content={
            "message": "login successful"
        }
    )

    response.set_cookie(
        key="access-token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400,
    )

    return response

@user_routes.get("/profile", response_model=UserGet, status_code=status.HTTP_200_OK)
def profile(request : Request):
    return request.state.user

@user_routes.get("/get_user")
def get(body:UserRegister):
    return get_user(body)

@user_routes.delete("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access-token",
        path="/"
    )

    return {
        "message": "Logout successful"
    }



    