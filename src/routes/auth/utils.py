from datetime import datetime, timedelta
import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pytz

SECRET_KEY = "gangster_lean_boogie"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_NEVER = 999


def create_access_token(username: str):
    """
    Utility function to create a new access token with expiration.
    """
    # need to convert to local timezone
    local_tz = pytz.timezone('US/Eastern')
    local_now = datetime.now(local_tz)

    expire = local_now + timedelta(days=ACCESS_TOKEN_EXPIRE_NEVER)
    to_encode = {
        "username": username,
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
        local_tz = pytz.timezone('US/Eastern')
        expiration = datetime.fromtimestamp(payload.get("exp"))
        expiration = local_tz.localize(expiration)

        # need to convert to local timezone
        local_now = datetime.now(local_tz)
        if local_now > expiration:
            print("Token has expired")
            raise HTTPException(
                status_code=401, detail="Access token has expired")

        return payload  # or simply True if you don't need to return payload details

    except jwt.PyJWTError:
        print("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        print("Exception: ", e)
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
