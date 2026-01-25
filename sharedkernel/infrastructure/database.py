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

        Args:
            stream_id: The unique identifier of the stream.
            events: A sequence of domain events to append.
            stream_type: The type of the stream (typically the aggregate class name).
            stream_slug: A human-readable identifier for the stream.
            stream_version: The version of the stream before appending.
            correlation_id: The correlation ID for this operation.

        Returns:
            The event position in the stream.
        """

    @abstractmethod
    def get_all(self, stream_id: UUID, from_version: int) -> Sequence[E]:
        """Fetch all events of a stream in this event store after a specific version.

        Args:
            stream_id: The unique identifier of the stream.
            from_version: The version to start retrieving events from.

        Returns:
            A sequence of events.
        """

    @abstractmethod
    def get_last(self, stream_id: UUID, types: List[type]) -> Optional[E]:
        """Fetch the latest event of the specified types for a stream.

        Args:
            stream_id: The unique identifier of the stream.
            types: A list of event classes to match.

        Returns:
            The most recent matching event, or None if not found.
        """

    @abstractmethod
    def get_stream(self, stream_id: UUID) -> Optional[S]:
        """Retrieves a single stream by its identifier.

        Args:
            stream_id: The unique identifier of the stream.

        Returns:
            The stream state, or None if not found.
        """

    @abstractmethod
    def get_streams_by_slug(self, slug: str, stream_type: str) -> Sequence[S]:
        """Retrieves all streams of a specific type that match the given slug.

        Args:
            slug: The slug identifier.
            stream_type: The type of the streams to search for.

        Returns:
            A sequence of stream states.
        """

    @abstractmethod
    def get_streams_by_type(self, stream_type: str) -> Sequence[S]:
        """Retrieves all streams of a given type.

        Args:
            stream_type: The type name.

        Returns:
            A sequence of stream states.
        """

    @abstractmethod
    def get_position(self, entity_id: UUID, event_type: str, stream_type: str) -> int:
        """Find the processed position in the transactional inbox for a given entity.

        Args:
            entity_id: The identifier of the entity.
            event_type: The type of the event.
            stream_type: The type of the stream.

        Returns:
            The current position.
        """

    @abstractmethod
    def update_position(self, entity_id: UUID, event_type: str, stream_type: str, position: int) -> None:
        """Insert or update the domain event position in the inbox for a given entity.

        Args:
            entity_id: The identifier of the entity.
            event_type: The type of the event.
            stream_type: The type of the stream.
            position: The new position to record.
        """
