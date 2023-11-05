from datetime import datetime, timedelta
import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pytz

from .schema import JWTData
# Change this to use secrets manager at some point
SECRET_KEY = "gangster_lean_boogie"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_NEVER = 999

def jwt_decode(encoded_jwt: str) -> JWTData:
    payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    return JWTData(**payload)