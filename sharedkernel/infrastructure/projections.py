from logging import Logger
from abc import abstractmethod, ABC
from types import get_original_bases
from typing import TypeVar, Generic, List, get_args
from uuid import UUID

from typeinspection import gethandledtypes

from sharedkernel.domain.errors import UnknownEvent
from sharedkernel.domain.events import DomainEvent, TEvent
from sharedkernel.infrastructure.data import DataModel
from sharedkernel.infrastructure.errors import OutOfOrderEvent

TModel = TypeVar("TModel", bound=DataModel)


class Projection(ABC, Generic[TModel]):

    @property
    def model_type(self) -> str:
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    @abstractmethod
    def get_position(self, entity_id: UUID, event_type: str) -> int:
        ...

    def apply(self, event: DomainEvent) -> None:
        raise UnknownEvent(self, event)

    @abstractmethod
    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        ...


TProjection = TypeVar("TProjection", bound=Projection)


class Projector(Generic[TProjection]):

    def __init__(self, logger: Logger, projection: Projection):
        self._logger = logger
        self.projection = projection

    @property
    def handles(self) -> List[str]:
        return gethandledtypes(type(self.projection))

    def process(self, event: TEvent, position: int, entity_id: UUID) -> None:
        current_position = self.projection.get_position(entity_id, event.qualname)

        event_type = type(event).__name__
        if position < current_position + 1:
            self._logger.debug(f"{event_type} position {position} has been already applied to Projection {entity_id}")
            return

        if position > current_position + 1:
            self._logger.error(f"{event_type} position {position} is out of order in Projection {entity_id}")
            raise OutOfOrderEvent(self.projection, str(entity_id), position)

        self.projection.apply(event)
        self._logger.info(f"{event_type} position {position} has been projected to record {entity_id}")

        self.projection.update_position(entity_id, event.qualname, position)
        self._logger.debug(f"{event_type} at Projection {entity_id} has been updated to position {position}")
