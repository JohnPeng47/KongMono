from fastapi.exceptions import HTTPException

class DuplicateUserException(HTTPException):
    def __init__(self, status_code=409, detail="User email already exists"):
        super().__init__(status_code=status_code, 
                         detail=detail)

class MissingUserException(HTTPException):
    def __init__(self, status_code=409, detail="User does not exist"):
        super().__init__(status_code=status_code, 
                         detail=detail)


class UserDoesNotExist(Exception):
    pass

class InvalidJWTDecode(Exception):
    # def __ini__()
    pass