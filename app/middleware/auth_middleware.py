#auth_middleware.py
from fastapi import Response, Request, HTTPException, status
from bson import ObjectId
from app.utils.security import verify_access_token
from app.config.database import get_user_collection
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

users = get_user_collection()

PUBLIC_ROUTES = [
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/user/login",
    "/user/register",
    "/livechart"
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):

        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)
        
        token = request.cookies.get("access-token")
        
        if not token :
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization Required"}
            )
            
        try:
            #jwt verify
            payload = verify_access_token(token)

            #paylaod se user id nikali
            user_id = payload["sub"]

            #find user from database through user id 
            current_user = users.find_one({"_id":ObjectId(user_id)})

            #user mila y nhi 
            if not current_user:
                return JSONResponse(
                    status_code=404,
                    content={'detail':"User Not Found"}
                )
            
            #clean response
            current_user["_id"] = str(current_user["_id"])
            current_user.pop("password",None)
            
            #request me user store kiya
            request.state.user = current_user

        except Exception:
            return JSONResponse(
                status_code=401,
                content={"detail":"Invalid Or Expired Token"}
            )

        # route execute 
        response = await call_next(request)
           
        return response

        

        

       