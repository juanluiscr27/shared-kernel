from collections import deque
from typing import get_args, Generic, TypeVar, Deque, List
from abc import abstractmethod, ABC
from types import get_original_bases
from typing import Dict, Any, Optional, Self

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import Event

TEvent = TypeVar("TEvent", bound=DomainEvent)


def to_event(message: Dict[str, Any], context: Any):
    return Event(
        event_id=message['id'],
        event_type=message['type'],
        position=message['position'],
        data=message['data'],
        stream_id=message['stream_id'],
        stream_type=message['stream_type'],
        version=message['version'],
        created=message['created'],
        correlation_id=message['correlation_id'],
    )


class Mapper(ABC, Generic[TEvent]):

    def __init__(self):
        self._next: Optional[Self] = None

    @property
    def event_type(self) -> str:
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    def set_next(self, mapper: Self):
        self._next = mapper

    @abstractmethod
    def map(self, data: Dict[str, Any], event_type: str) -> Optional[TEvent]:
        ...

    def map_next(self, data: Dict[str, Any], event_type: str) -> Optional[DomainEvent]:
        if not self._next:
            return None

        return self._next.map(data, event_type)


class MappingBehavior(ABC):

    @abstractmethod
    def map(self, data: Dict[str, Any], event_type: str) -> Optional[DomainEvent]:
        ...


class MappersChain(MappingBehavior):

    def __init__(self):
        self._mappers: Deque[Mapper] = deque()
        self._first: Optional[Mapper] = None

    def add(self, mapper: Mapper) -> None:
        if self._first:
            mapper.set_next(self._first)

        self._mappers.appendleft(mapper)
        self._first = mapper

    def map(self, data: Dict[str, Any], event_type: str) -> Optional[DomainEvent]:
        if not self._first:
            return None

        return self._first.map(data, event_type)


class MappingPipeline:

    def __init__(self):
        self._chain: List[MappingBehavior] = list()

    def register(self, behavior: MappingBehavior):
        self._chain.append(behavior)

    def map(self, data: Dict[str, Any], event_type: str) -> Optional[DomainEvent]:
        for behavior in self._chain:
            event = behavior.map(data, event_type)

            if event:
                return event

        return None
