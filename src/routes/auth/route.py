from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .schema import User, AuthenticateRequest
from .db import create_db_user
from .utils import create_access_token

from typing import List

router = APIRouter()


@router.post("/user/")
def create_user(user: User):
    result = create_db_user(user)
    if result.inserted_id:
        # Generate token
        access_token = create_access_token(user.username)

        response = JSONResponse(
            content={"msg": "User created successfully"}, status_code=status.HTTP_201_CREATED)
        # Set token as a cookie
        response.set_cookie(key="access_token",
                            value=access_token, httponly=True)

        return response
    else:
        raise HTTPException(
            status_code=500, detail="An error occurred while inserting the user.")


@router.post("/authenticate/")
def authenticate_user(request: AuthenticateRequest):
    return {"token": create_access_token(request.username)}
