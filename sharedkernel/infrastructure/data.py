from dataclasses import dataclass


@dataclass(frozen=True)
class DataModel:
    """DataModel base class

    Is a Data Transfer Object representing cohesive information in the infrastructure optimized for queries.
    """


@dataclass(frozen=True)
class Event(DataModel):
    event_id: str
    event_type: str
    position: int
    data: str
    stream_id: str
    stream_type: str
    version: int
    created: str


@dataclass(frozen=True)
class Message:
    message_id: str
    content_type: str
    subject: str
    body: str
