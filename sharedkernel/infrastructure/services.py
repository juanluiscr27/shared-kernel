import json
import typing
from types import get_original_bases
from typing import List

from sharedkernel.domain.events import DomainEvent, DomainEventHandler
from sharedkernel.infrastructure.data import Event
from sharedkernel.infrastructure.errors import MapperNotFound, UnsupportedEventHandler, UnprocessableListener
from sharedkernel.infrastructure.mappers import MappingPipeline
from sharedkernel.infrastructure.projections import Projector

TEventHandler = typing.TypeVar("TEventHandler", bound=DomainEventHandler)


class EventBroker:
    """
    Mediates the communication of event messages between producers and consumers.

    Notify consumers when a new message is received.
    """

    def __init__(self):
        self._consumers: dict[str, list[TEventHandler]] = dict()

    def subscribe(self, event_handler: TEventHandler) -> bool:
        """Subscribe a Domain Event Handler as consumers to an Event Group.

        Args:
            event_handler: Event Consumer that will process a specific kind of
            event when published.

        Returns:
            True if the Event Handler was successfully subscribed, otherwise False.
        """
        handler_type = type(event_handler).__name__
        if not isinstance(event_handler, DomainEventHandler):
            raise UnsupportedEventHandler(self, handler_type)

        bases = get_original_bases(event_handler.__class__)
        args = typing.get_args(bases[0])
        event_type = args[0].__name__

        if event_type in self._consumers:
            self._consumers[event_type].append(event_handler)
        else:
            self._consumers[event_type] = [event_handler]

        return True

    def publish(self, event: DomainEvent) -> None:
        """Publish a Domain Event to its respective Event Group.

        Look for the Handlers subscribed in the Domain Event Group and notify
        them to process the Event.

        Args:
           event: Domain Event to publish.

        Returns:
           None
        """
        event_type = type(event).__name__

        if event_type not in self._consumers:
            return

        consumer_group = self._consumers[event_type]

        for consumer in consumer_group:
            consumer.process(event)


class EventDispatcher:
    """
    A Dispatcher is a service object that is given an Event object by an Emitter.

    The Dispatcher is responsible for ensuring that the Event is passed to all relevant Listeners.
    """

    def __init__(self, mapper: MappingPipeline):
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
        if not handled_types:
            listener_name = type(listener).__name__
            raise UnprocessableListener(self, listener_name)

        for event_type in handled_types:
            if event_type in self._listeners:
                self._listeners[event_type].append(listener)
            else:
                self._listeners[event_type] = [listener]

        return True

    def dispatch(self, event: Event) -> None:
        """Publish a Domain Event to its respective Event Group.

        Look for the Handlers subscribed in the Event Group and notify them to process the Event.

        Args:
           event: Event to dispatch.

        Returns:
           None

        Raises:
            MapperNotFound
        """
        event_type = event.event_type

        if event_type not in self._listeners:
            return

        event_data = json.loads(event.data)

        domain_event = self._mapper.map(event_data, event_type)
        if not domain_event:
            raise MapperNotFound(self, event_type)

        listener_group = self._listeners[event_type]

        for listener in listener_group:
            listener.process(domain_event, event.position)
