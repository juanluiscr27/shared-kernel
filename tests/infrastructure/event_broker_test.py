from dataclasses import dataclass

from sharedkernel.domain.events import DomainEvent, DomainEventHandler
from sharedkernel.infrastructure.services import EventBroker


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    event_id: str
    message: str


@dataclass(frozen=True)
class UserLoggedIn(DomainEvent):
    event_id: str
    message: str


class RegistrationEventHandler(DomainEventHandler):

    def process(self, event: UserRegistered):
        print(f"{event.event_id} event processed by {self.__class__}")


def test_event_handler_is_subscribed_to_event_broker():
    # Arrange
    event_handler = RegistrationEventHandler()
    event_broker = EventBroker()

    # Act
    result = event_broker.subscribe(event_handler)

    # Assert
    assert result is True


def test_other_object_cannot_be_subscribed_to_event_broker():
    # Arrange
    not_event_handler = DomainEvent()
    event_broker = EventBroker()

    # Act
    # noinspection PyTypeChecker
    result = event_broker.subscribe(not_event_handler)

    # Assert
    assert result is False


def test_domain_event_is_processed_by_subscribed_handler(capture_stdout):
    # Arrange
    event_handler = RegistrationEventHandler()
    event_broker = EventBroker()
    subscription_result = event_broker.subscribe(event_handler)
    console = ("UserRegistered event processed by <class "
               "'tests.infrastructure.event_broker_test.RegistrationEventHandler'>\n")

    # Act
    event = UserRegistered(event_id="UserRegistered", message="User(name='John Doe')")
    event_broker.publish(event)

    # Assert
    assert subscription_result is True
    assert capture_stdout["console"] == console
