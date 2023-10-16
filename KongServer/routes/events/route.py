from fastapi import APIRouter, FastAPI, Depends
from ..auth.utils import get_username_from_token
from .schema import TrackingEvent
from fastapi.requests import Request


router = APIRouter()
app = FastAPI()


@router.post("/events", )
def events(event: TrackingEvent, request: Request, username: str = Depends(get_username_from_token)):
    print("Event: ", event, "user: ", username)
    request.app.queue.append(
        username,
        {"hello": "world"}
    )
    return {"username": username}
