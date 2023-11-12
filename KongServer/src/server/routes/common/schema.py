from pydantic import BaseModel, Field

class RequestSuccess(BaseModel):
    message: str = "Success!"