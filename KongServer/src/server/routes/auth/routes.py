from fastapi import APIRouter, HTTPException, status, Depends, Body

from .exceptions import DuplicateUserException, MissingUserException
from .schema import User, RegisterUserResponse, UserAuthRequest
from .service import get_user_by_id, create_user, delete_user, get_user_by_email, user_email_checker, create_access_token

from src.server.routes.common.schema import RequestSuccess

router = APIRouter()

@router.post("/register")
def register_user_route(authReq: UserAuthRequest = Body(...),
                user: bool = Depends(get_user_by_email)) -> User:
    if user:
        raise DuplicateUserException

    # not handling case of mongoDB failure
    user = create_user(user)

    return {
        "message" : "success",
        "user_id" : user.id
    }

@router.get("/delete/{user_id}",
             response_model=RegisterUserResponse)
def delete_user_route(user_id: str,
                      user: bool = Depends(get_user_by_id)):
    if not user:
        raise MissingUserException
        
    delete_user(user_id)

    return {
        "message": "success"
    }

@router.post("/authenticate/")
def authenticate_user_route(user: UserAuthRequest):
    user = get_user_by_email(user)
    if not user:
        return MissingUserException
    
    return {
        "token": create_access_token(user.email)
    }
