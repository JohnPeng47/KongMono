from pydantic import BaseModel


class ReadDescriptionEventData(BaseModel):
    node_id: str


class ReadDescriptionEvent(BaseModel):
    eventType: str
    data: ReadDescriptionEventData


class TrackingEvent(BaseModel):
    event: ReadDescriptionEvent
