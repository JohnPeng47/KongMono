from fastapi import APIRouter, FastAPI, Depends
from ..auth.service import get_user_from_token
from .schema import TrackingEvent
from fastapi.requests import Request


router = APIRouter()
app = FastAPI()

@router.post("/events", )
def events(event: TrackingEvent, 
           request: Request, 
           email: str = Depends(get_user_from_token)):
    print("Event: ", event, "user: ", email)
    return {"username": email}