import re
from datetime import datetime
from typing import List
from pydantic import Field, validator, BaseModel
from pydantic import EmailStr

from uuid import uuid4

from fastapi.exceptions import HTTPException
from email_validator import validate_email, EmailNotValidError 

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")

class WeakPasswordError(Exception):
    def __init__(self):
        super().__init__(message = """
                Password must contain at least
                one lower character, 
                one upper character, digit or special symbol
            """)
class InvalidEmailError(Exception):
    def __init__(self):
        super().__init__(message="Invalid email format")

class UserAuthRequest(BaseModel):
    # change at your own risk
    email: str
    password: str = Field(min_length=6, max_length=128)

    @validator("password")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise WeakPasswordError()
        return password

    @validator("email")
    @classmethod
    def valid_email(cls, email: str) -> str:
        try:
            validate_email(email)
            return email
        except EmailNotValidError:
            raise InvalidEmailError()
        
class User(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=128)
    graphs: List[str] = Field(default_factory=list)
    id: str = Field(default_factory=lambda: str(uuid4()))

    @validator("password")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise WeakPasswordError()
        return password

    @validator("email")
    @classmethod
    def valid_email(cls, email: str) -> str:
        try:
            validate_email(email)
            return email
        except EmailNotValidError:
            raise InvalidEmailError()

        
class RegisterUserResponse(BaseModel):
    email: str

class JWTData(BaseModel):
    email: str
    exp: datetime
