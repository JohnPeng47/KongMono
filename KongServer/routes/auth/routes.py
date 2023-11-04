from fastapi import APIRouter, HTTPException, status, Depends

from .exceptions import DuplicateUserException
from .schema import AuthUser, RegisterUserResponse
from .utils import create_access_token
from .service import create_user, get_user_by_email, user_email_checker, create_access_token

router = APIRouter()

@router.post("/register", 
             status_code=status.HTTP_201_CREATED, 
             response_model=RegisterUserResponse)
def register_user(user: AuthUser = Depends(user_email_checker)) -> AuthUser:
    try: 
        res = create_user(user)
        return {
            "email" : user.email
        }
    except DuplicateUserException:
        raise HTTPException(
            status_code=409, detail="User email already exists"
        )   

@router.post("/authenticate/")
def authenticate_user(user: AuthUser):
    user = get_user_by_email(user.email)
    
    return {
        "token": create_access_token(user.email)
    }