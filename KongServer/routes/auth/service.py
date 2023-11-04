from pydantic import EmailStr

from datetime import datetime, timedelta
import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pytz

from .schema import AuthUser
from .exceptions import DuplicateUserException
from .config import ACCESS_TOKEN_EXPIRE_DAYS

from database import db_conn
from database.exceptions import MongoUnacknowledgeError 

from logging import getLogger

logger = getLogger("server")

# Change this to use secrets manager at some point
SECRET_KEY = "gangster_lean_boogie"
ALGORITHM = "HS256"

def create_user(user: AuthUser) -> AuthUser:
    res = db_conn.get_collection("users").insert_one(user.dict())

    # IDK about this exception
    if not res.acknowledged:
        raise MongoUnacknowledgeError("User creation Unacknowledged")
    
    return True
    
def get_user_by_email(email: EmailStr) -> AuthUser | None:
    user_dict = db_conn.get_collection("users").find_one({
        "email" : email
    })

    if user_dict:
        return AuthUser(**user_dict)
    
    return None

def user_email_checker(user: AuthUser) -> AuthUser | None:
    user_exists = get_user_by_email(user.email)
    # TODO: this error is not getting caught
    if user_exists:
        raise DuplicateUserException(f"User with email: {user.email} already exists")
    return user

def create_access_token(username: str):
    """
    Utility function to create a new access token with expiration.
    """
    # need to convert to local timezone
    local_tz = pytz.timezone('US/Eastern')
    local_now = datetime.now(local_tz)

    expire = local_now + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "email": username,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# probably should make this depend on another dependency to retrieve the user
def validate_token(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Validate the JWT token from the request's Authorization header.
    """
    token = authorization.credentials
    try:
        # Decoding the token using the SECRET_KEY and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if the token has expired
        # local_tz = pytz.timezone('US/Eastern')
        # expiration = datetime.fromtimestamp(payload.get("exp"))
        # expiration = local_tz.localize(expiration)

        # # need to convert to local timezone
        # local_now = datetime.now(local_tz)
        # if local_now > expiration:
        #     logger.debug(f"Token has expired for user {payload.email}")
        #     raise HTTPException(
        #         status_code=401, detail="Access token has expired")

        return payload  # or simply True if you don't need to return payload details
    
    except jwt.ExpiredSignatureError:
        user = payload.get("email")
        logger.debug(f"Token for user {user} has expired")
        raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_username_from_token(decoded_token: dict = Depends(validate_token)) -> str:
    """
    Extract the username from the decoded JWT token.
    """
    # Extracting username from the decoded token
    print("Token: ", decoded_token)
    username = decoded_token.get("username")

    # If username isn't present in the decoded token, raise an error
    if not username:
        raise HTTPException(
            status_code=400, detail="Username not present in the token")

    return username