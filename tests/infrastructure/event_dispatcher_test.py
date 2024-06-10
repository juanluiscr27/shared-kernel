from dataclasses import dataclass
from functools import singledispatchmethod

import pytest

from sharedkernel.domain.events import DomainEvent
from sharedkernel.infrastructure.data import DataModel, Event
from sharedkernel.infrastructure.errors import UnprocessableListener
from sharedkernel.infrastructure.projections import Projector, Projection
from sharedkernel.infrastructure.services import EventDispatcher, MappingPipeline


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    name: str
    slug: str


@dataclass(frozen=True)
class UserNameUpdated(DomainEvent):
    user_id: int
    new_name: str
    previous_name: str


class UserModel(DataModel):
    user_id: int
    name: str
    slug: str


class UserDetailsProjection(Projection[UserModel]):

    @singledispatchmethod
    def apply(self, event: DomainEvent) -> None:
        super().apply(event)

    @apply.register
    def _when(self, event: UserRegistered) -> None:
        pass

    @apply.register
    def _when(self, event: UserNameUpdated) -> None:
        pass


class UserListProjection(Projection[UserModel]):

    @singledispatchmethod
    def apply(self, event: DomainEvent) -> None:
        super().apply(event)


class UserDetailsProjector(Projector[UserDetailsProjection]):

    def process(self, event: DomainEvent, position: int, version: int) -> None:
        print(f"{event.__class__.__name__} event processed by '{self.__class__.__name__}'")


class UserListProjector(Projector[UserListProjection]):

    def process(self, event: DomainEvent, position: int, version: int) -> None:
        pass


class FakeDomainEventMapper(MappingPipeline):

    def map(self, data: dict, data_type: str):
        return UserRegistered(user_id=101, name="John Doe Smith", slug="john-doe-smith")


def test_projector_is_subscribed_to_event_dispatcher(fake_logger):
    # Arrange
    projector = UserDetailsProjector()
    fake_mapper = FakeDomainEventMapper()
    event_dispatcher = EventDispatcher(logger=fake_logger, mapper=fake_mapper)

    # Act
    result = event_dispatcher.subscribe(projector)

    # Assert
    assert result is True


def test_projector_with_no_handled_event_raise_error(fake_logger):
    # Arrange
    projector = UserListProjector()
    fake_mapper = FakeDomainEventMapper()
    event_dispatcher = EventDispatcher(logger=fake_logger, mapper=fake_mapper)

    # Act
    with pytest.raises(UnprocessableListener) as error:
        event_dispatcher.subscribe(projector)

    # Assert
    assert str(error.value) == "Cannot subscribe `UserListProjector` because it does not handle any event"


def test_event_is_processed_by_subscribed_handler(fake_logger, capture_stdout):
    # Arrange
    event = Event(
        event_id="018f55de-8321-7efd-a4e3-fcc2c5ec5eea",
        event_type="UserRegistered",
        position=1,
        data='{"user_id":101,   "name":"John Doe Smith",   "slug":"john-doe-smith"}',
        stream_id="101",
        stream_type="User",
        version=1,
        created='2024-04-28T12:30−04:00',
        correlation_id='018fa862-800b-7b6a-8690-ba0e06908c26'
    )

    event_handler = UserDetailsProjector()
    fake_mapper = FakeDomainEventMapper()
    event_dispatcher = EventDispatcher(logger=fake_logger, mapper=fake_mapper)
    subscription_result = event_dispatcher.subscribe(event_handler)
    console = "UserRegistered event processed by 'UserDetailsProjector'\n"

    # Act
    event_dispatcher.dispatch(event)

    # Assert
    assert subscription_result is True
    assert capture_stdout["console"] == console
