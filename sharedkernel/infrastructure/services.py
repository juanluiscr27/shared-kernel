import json
import typing
from datetime import datetime
from logging import Logger
from types import get_original_bases
from typing import List, TypeVar, Any
from uuid import UUID

from sharedkernel.domain.events import DomainEvent, DomainEventHandler
from sharedkernel.infrastructure.data import Event
from sharedkernel.infrastructure.errors import MapperNotFound, UnsupportedEventHandler, UnprocessableListener
from sharedkernel.infrastructure.mappers import MappingPipeline
from sharedkernel.infrastructure.projections import Projector

TEventHandler = TypeVar("TEventHandler", bound=DomainEventHandler)


class UUIDEncoder(json.JSONEncoder):
    """JSON encoder that supports UUID objects."""

    def default(self, obj: Any) -> Any:
        """Encodes UUID objects as strings."""
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that supports datetime objects."""

    def default(self, obj: Any) -> Any:
        """Encodes datetime objects as ISO format strings."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class ExtraEncoder(json.JSONEncoder):
    """JSON encoder that supports both UUID and datetime objects."""

    def default(self, obj: Any) -> Any:
        """Encodes UUID and datetime objects as strings."""
        if isinstance(obj, UUID):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


class EventBroker:
    """Mediates the communication of event messages between producers and consumers.

    The Event Broker acts as an in-memory pub-sub mechanism, notifying registered consumers
    (DomainEventHandlers) when a domain event is published.

    Args:
        logger: The logger instance.
    """

    def __init__(self, logger: Logger):
        self._logger = logger
        self._consumers: dict[str, list[TEventHandler]] = dict()

    def subscribe(self, event_handler: TEventHandler) -> bool:
        """Subscribe a Domain Event Handler as consumers to an Event Group.

        Args:
            event_handler: Event Consumer that will process a specific kind of event when published.

        Returns:
            True if the Event Handler was successfully subscribed, otherwise False.
        """
        handler_type = type(event_handler).__name__
        if not isinstance(event_handler, DomainEventHandler):
            self._logger.error(f"{handler_type} is not a valid Domain Event Handler")
            raise UnsupportedEventHandler(self, handler_type)

        bases = get_original_bases(event_handler.__class__)
        args = typing.get_args(bases[0])
        event_type = args[0].__name__

        if event_type in self._consumers:
            self._consumers[event_type].append(event_handler)
        else:
            self._consumers[event_type] = [event_handler]

        self._logger.debug(f"{handler_type} was successfully subscribed")
        return True

    def publish(self, event: DomainEvent, position: int) -> None:
        """Publish a Domain Event to its respective Event Group.

        Look for the Handlers subscribed in the Domain Event Group and notify
        them to process the Event.

        Args:
           event: Domain Event to publish.
           position: Event position at the Stream

        Returns:
           None
        """
        event_type = type(event).__name__

        if event_type not in self._consumers:
            self._logger.debug(f"No handler subscribed for {event_type} event")
            return

        consumer_group = self._consumers[event_type]

        self._logger.info(f"{event_type} event was published")
        for consumer in consumer_group:
            consumer.process(event, position)


class EventDispatcher:
    """Service that dispatches raw infrastructure events to interested listeners.

    The dispatcher uses a MappingPipeline to convert raw event data into domain events
    and then routes them to registered Projectors or other listeners.
    """

    def __init__(self, logger: Logger, mapper: MappingPipeline):
        """Initializes an EventDispatcher.

        Args:
            logger: The logger instance.
            mapper: The mapping pipeline to convert raw events to domain events.
        """
        self._logger = logger
        self._mapper = mapper
        self._listeners: dict[str, List[Projector]] = dict()

    def subscribe(self, listener: Projector) -> bool:
        """Subscribe an Event Handler as listener to an Event Group.

        Args:
            listener: Is callable that expects to be passed an Event and a sequential position.

        Returns:
            True if the Event Handler was successfully subscribed, otherwise False.
        """
        handled_types = listener.handles
        listener_name = f"{type(listener).__name__} of {type(listener.projection).__name__}"
        if not handled_types:
            self._logger.error(f"Listener {listener_name} does not handle any type")
            raise UnprocessableListener(self, listener_name)

        for event_type in handled_types:
            if event_type in self._listeners:
                self._listeners[event_type].append(listener)
            else:
                self._listeners[event_type] = [listener]

        self._logger.debug(f"{listener_name} was successfully subscribed")
        return True

    def dispatch(self, event: Event) -> None:
        """Publish a Domain Event to its respective Event Group.

        Look for the Handlers subscribed in the Event Group and notify them to process the Event.

        Args:
           event: Event to dispatch.

        Returns:
           None

        Raises:
            MapperNotFound: If the MappingPipeline does not have any event mapper for the given event type name.
        """
        event_type = event.event_type

        if event_type not in self._listeners:
            self._logger.debug(f"No listener subscribed for {event_type} event")
            return

        event_data = json.loads(event.data)

        domain_event = self._mapper.map(event_data, event_type)
        if not domain_event:
            self._logger.error(f"MappingPipeline does not have any event mapper for {event_type}")
            raise MapperNotFound(self, event_type)

        listener_group = self._listeners[event_type]

        self._logger.info(f"{event_type} event dispatched to all listeners")
        for listener in listener_group:
            listener.process(domain_event, event.position, event.stream_id)
