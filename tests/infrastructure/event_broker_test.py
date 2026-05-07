from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import pytest

from sharedkernel.application.commands import Command, CommandHandler
from sharedkernel.application.services import get_request_id
from sharedkernel.domain.events import DomainEvent, DomainEventHandler
from sharedkernel.infrastructure.data import Event
from sharedkernel.infrastructure.exceptions import UnsupportedEventHandler
from sharedkernel.infrastructure.mappers import MappingPipeline
from sharedkernel.infrastructure.services import EventBroker


@dataclass(frozen=True)
class RegisterUser(Command):
    user_id: UUID
    name: str
    slug: str


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    event_id: str
    message: str


@dataclass(frozen=True)
class UserLoggedIn(DomainEvent):
    event_id: str
    message: str


class RegistrationEventHandler(DomainEventHandler[UserRegistered]):

    def process(self, event: UserRegistered, position: int):
        print(f"{event.event_id} event processed by {type(self).__name__}")


class EmailUserEventHandler(DomainEventHandler[UserRegistered]):

    def process(self, event: UserRegistered, position: int):
        print(f"{event.event_id} event processed by {type(self).__name__}")


class ContextAwareEventHandler(DomainEventHandler[UserRegistered]):

    def process(self, event: UserRegistered, position: int):
        print(f"{event.event_id} event processed with request_id={get_request_id()}")


class RegisterUserCommandHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser):
        pass


class FakeDomainEventMapper(MappingPipeline):

    def map(self, data: dict, data_type: str):
        return UserRegistered(
            event_id=data.get("event_id", "UserRegistered"),
            message=data.get("message", "User(name='John Doe')")
        )


class NoDomainEventMapper(MappingPipeline):

    def map(self, _: dict, __: str):
        return None


def test_event_handler_is_subscribed_to_event_broker(fake_logger):
    # Arrange
    event_handler = RegistrationEventHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)

    # Act
    result = event_broker.subscribe(event_handler)

    # Assert
    assert result is True


def test_two_event_handlers_are_subscribed_to_event_broker(fake_logger):
    # Arrange
    registration_handler = RegistrationEventHandler()
    email_handler = EmailUserEventHandler()

    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)

    # Act
    result1 = event_broker.subscribe(registration_handler)
    result2 = event_broker.subscribe(email_handler)

    # Assert
    assert result1 is True
    assert result2 is True


def test_subscribe_not_event_handler_to_event_broker_raise_error(fake_logger):
    # Arrange
    expected = "`RegisterUserCommandHandler` cannot be registered to EventBroker"

    command_handler = RegisterUserCommandHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)

    # Act
    with pytest.raises(UnsupportedEventHandler) as error:
        # noinspection PyTypeChecker
        _ = event_broker.subscribe(command_handler)

    # Assert
    assert str(error.value) == expected


def test_domain_event_is_processed_by_subscribed_handler(fake_logger, capture_stdout):
    # Arrange
    event_handler = RegistrationEventHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)
    subscription_result = event_broker.subscribe(event_handler)
    console = "UserRegistered event processed by RegistrationEventHandler\n"

    # Act
    event = Event(
        event_id=UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea"),
        event_type="UserRegistered",
        position=1,
        data='{"event_id":"UserRegistered", "message":"User(name=\'John Doe\')"}',
        stream_id=UUID("018f9284-769b-726d-b3bf-3885bf2ddd3c"),
        stream_type="User",
        version=1,
        created=datetime.fromisoformat('2024-04-28T12:30:12-04:00'),
        correlation_id=UUID('018fa862-800b-7b6a-8690-ba0e06908c26'),
    )
    event_broker.publish(event)

    # Assert
    assert subscription_result is True
    assert capture_stdout["console"] == console


def test_domain_event_is_not_processed_when_no_subscribed_handler(fake_logger, capture_stdout):
    # Arrange
    event_handler = RegistrationEventHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)
    subscription_result = event_broker.subscribe(event_handler)

    # Act
    event = Event(
        event_id=UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea"),
        event_type="UserLoggedIn",
        position=1,
        data='{"event_id":"UserLoggedIn", "message":"User(name=\'John Doe\')"}',
        stream_id=UUID("018f9284-769b-726d-b3bf-3885bf2ddd3c"),
        stream_type="User",
        version=1,
        created=datetime.fromisoformat('2024-04-28T12:30:12-04:00'),
        correlation_id=UUID('018fa862-800b-7b6a-8690-ba0e06908c26'),
    )
    event_broker.publish(event)

    # Assert
    assert subscription_result is True
    assert not capture_stdout["console"]


def test_domain_event_is_not_processed_when_no_mapper_found(fake_logger, capture_stdout):
    # Arrange
    event_handler = RegistrationEventHandler()
    no_mapper = NoDomainEventMapper()
    event_broker = EventBroker(fake_logger, no_mapper)
    subscription_result = event_broker.subscribe(event_handler)

    # Act
    event = Event(
        event_id=UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea"),
        event_type="UserRegistered",
        position=1,
        data='{"event_id":"UserRegistered", "message":"User(name=\'John Doe\')"}',
        stream_id=UUID("018f9284-769b-726d-b3bf-3885bf2ddd3c"),
        stream_type="User",
        version=1,
        created=datetime.fromisoformat('2024-04-28T12:30:12-04:00'),
        correlation_id=UUID('018fa862-800b-7b6a-8690-ba0e06908c26'),
    )
    event_broker.publish(event)

    # Assert
    assert subscription_result is True
    assert not capture_stdout["console"]


def test_event_handler_sees_correct_request_id_when_event_is_published(fake_logger, capture_stdout):
    # Arrange
    handler = ContextAwareEventHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)
    event_broker.subscribe(handler)
    correlation_id = UUID('018fa862-800b-7b6a-8690-ba0e06908c26')
    console = f"UserRegistered event processed with request_id={correlation_id}\n"

    event = Event(
        event_id=UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea"),
        event_type="UserRegistered",
        position=1,
        data='{"event_id":"UserRegistered", "message":"User(name=\'John Doe\')"}',
        stream_id=UUID("018f9284-769b-726d-b3bf-3885bf2ddd3c"),
        stream_type="User",
        version=1,
        created=datetime.fromisoformat('2024-04-28T12:30:12-04:00'),
        correlation_id=correlation_id,
    )

    # Act
    event_broker.publish(event)

    # Assert
    assert capture_stdout["console"] == console


def test_request_id_is_reset_after_event_processing(fake_logger):
    # Arrange
    handler = ContextAwareEventHandler()
    fake_mapper = FakeDomainEventMapper()
    event_broker = EventBroker(fake_logger, fake_mapper)
    event_broker.subscribe(handler)
    correlation_id = UUID('018fa862-800b-7b6a-8690-ba0e06908c26')

    event = Event(
        event_id=UUID("018f55de-8321-7efd-a4e3-fcc2c5ec5eea"),
        event_type="UserRegistered",
        position=1,
        data='{"event_id":"UserRegistered", "message":"User(name=\'John Doe\')"}',
        stream_id=UUID("018f9284-769b-726d-b3bf-3885bf2ddd3c"),
        stream_type="User",
        version=1,
        created=datetime.fromisoformat('2024-04-28T12:30:12-04:00'),
        correlation_id=correlation_id,
    )

    # Act
    event_broker.publish(event)
    result = get_request_id()

    # Assert
    assert result != correlation_id
