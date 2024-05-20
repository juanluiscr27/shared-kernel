from dataclasses import dataclass
from uuid import UUID

import pytest

from sharedkernel.application.commands import Command, CommandHandler
from sharedkernel.domain.events import DomainEvent, DomainEventHandler
from sharedkernel.infrastructure.errors import UnsupportedEventHandler
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

    def process(self, event: UserRegistered):
        print(f"{event.event_id} event processed by {type(self).__name__}")


class RegisterUserCommandHandler(CommandHandler[RegisterUser]):

    def execute(self, command: RegisterUser):
        pass


def test_event_handler_is_subscribed_to_event_broker():
    # Arrange
    event_handler = RegistrationEventHandler()
    event_broker = EventBroker()

    # Act
    result = event_broker.subscribe(event_handler)

    # Assert
    assert result is True


def test_subscribe_not_event_handler_to_event_broker_raise_error():
    # Arrange
    expected = "`RegisterUserCommandHandler` cannot be registered to EventBroker"

    command_handler = RegisterUserCommandHandler()
    event_broker = EventBroker()

    # Act
    with pytest.raises(UnsupportedEventHandler) as error:
        # noinspection PyTypeChecker
        _ = event_broker.subscribe(command_handler)

    # Assert
    assert str(error.value) == expected


def test_domain_event_is_processed_by_subscribed_handler(capture_stdout):
    # Arrange
    event_handler = RegistrationEventHandler()
    event_broker = EventBroker()
    subscription_result = event_broker.subscribe(event_handler)
    console = "UserRegistered event processed by RegistrationEventHandler\n"

    # Act
    event = UserRegistered(event_id="UserRegistered", message="User(name='John Doe')")
    event_broker.publish(event)

    # Assert
    assert subscription_result is True
    assert capture_stdout["console"] == console
