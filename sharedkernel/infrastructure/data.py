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
    """Represents a domain event in the infrastructure layer.

    Attributes:
        event_id: Unique identifier for the event.
        event_type: The type name of the event.
        position: The sequential position of the event in the stream.
        data: The JSON-serialized event data.
        stream_id: The identifier of the aggregate stream.
        stream_type: The type name of the aggregate.
        version: The version of the aggregate at the time of the event.
        created: The timestamp when the event was created.
        correlation_id: Unique identifier to correlate events from related requests.
    """
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
    """Represents a generic message for cross-context communication.

    Attributes:
        message_id: Unique identifier for the message.
        content_type: The MIME type of the content.
        subject: The subject or topic of the message.
        body: The serialized content of the message.
    """
    message_id: UUID
    content_type: str
    subject: str
    body: str
