from typing import get_args
from abc import abstractmethod, ABC
from types import get_original_bases
from typing import TypeVar, Generic, List
from uuid import UUID

from typeinspection import gethandledtypes

from sharedkernel.domain.errors import UnknownEvent
from sharedkernel.domain.events import DomainEvent, TEvent

TModel = TypeVar("TModel")


class Projection(ABC, Generic[TModel]):
    @abstractmethod
    def get_position(self, entity_id: UUID, event_type: str) -> int:
        ...

    def apply(self, event: DomainEvent) -> None:
        raise UnknownEvent(self, event)

    @abstractmethod
    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        ...


TProjection = TypeVar("TProjection", bound=Projection)


class Projector(ABC, Generic[TProjection]):

    @property
    def handles(self) -> List[str]:
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return gethandledtypes(args[0])

    @abstractmethod
    def process(self, event: TEvent, position: int, version: int) -> None:
        ...
