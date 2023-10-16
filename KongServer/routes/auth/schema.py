from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    disabled: bool | None = None


class AuthenticateRequest(BaseModel):
    username: str
    # password: str
