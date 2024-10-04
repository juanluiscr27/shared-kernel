from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DataModel:
    """DataModel base class

    Is a Data Transfer Object representing cohesive information in the infrastructure optimized for queries.
    """


@dataclass(frozen=True)
class Event(DataModel):
    event_id: UUID
    event_type: str
    position: int
    data: str
    stream_id: UUID
    stream_type: str
    version: int
    created: datetime
    correlation_id: UUID


@dataclass(frozen=True)
class Message:
    message_id: UUID
    content_type: str
    subject: str
    body: str
