from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, List, Optional, Generic
from uuid import UUID

from sharedkernel.domain.events import DomainEvent

E = TypeVar("E")
S = TypeVar("S")


class EventStore(ABC, Generic[E, S]):
    """An event store is a database optimized for storage of events

    An Event Store acts as append-only log and records only the events of a given entity.
    The state of the entity at any point in its history can be reconstructed
    by replaying its corresponding events in sequential order.
    """

    @abstractmethod
    def append(
            self,
            stream_id: UUID,
            events: Sequence[DomainEvent],
            stream_type: str,
            stream_slug: str,
            stream_version: int,
            correlation_id: UUID,
    ) -> int:
        """Appends a sequence of events to a stream in this event store.

        Returns:
            The event position in the stream.
        """

    @abstractmethod
    def get_all(self, stream_id: UUID, from_version: int) -> Sequence[E]:
        """Retrieves all events of a stream in this event store from a specific version."""

    @abstractmethod
    def get_last(self, stream_id: UUID, types: List[type]) -> Optional[E]:
        """Retrieves last events of a stream that matches any of the given types"""

    @abstractmethod
    def get_stream(self, stream_id: UUID) -> Optional[S]:
        """Retrieves last events of a stream that matches any of the given types"""

    @abstractmethod
    def get_streams_by_slug(self, slug: str, stream_type: str) -> Sequence[S]:
        """Retrieves all streams that match the given slug of a specific type"""

    @abstractmethod
    def get_streams_by_type(self, stream_type: str) -> Sequence[S]:
        """Retrieves all streams that match the given type"""

    @abstractmethod
    def get_position(self, entity_id: UUID, event_type: str, stream_type: str) -> int:
        """Find the domain event position in the transactional inbox for a given entity"""

    @abstractmethod
    def update_position(self, entity_id: UUID, event_type: str, stream_type: str, position: int) -> None:
        """Insert or update the domain event position in the inbox for a given entity"""
