from inspect import signature

from sharedkernel.domain.events import DomainEvent, DomainEventHandler


class EventBroker:
    """
    Mediates the communication of event messages between producers and consumers.

    Notify consumers when a new message is received.
    """

    def __init__(self):
        self._consumers: dict[str, list[DomainEventHandler]] = dict()

    def subscribe(self, event_handler: DomainEventHandler) -> bool:
        """Subscribe a Domain Event Handler as consumers to an Event Group.

        Args:
            event_handler: Event Consumer that will process a specific kind of
            event when published.

        Returns:
            True if the Event Handler was successfully subscribed, otherwise False.
        """

        try:
            method_signature = signature(event_handler.process)
            parameters = method_signature.parameters
        except AttributeError as err:
            print(f"EventBroker.ConsumerSubscriptionError: {err}")
            return False

        if not parameters:
            return False

        parameter = next(iter(parameters.values()))
        event_type = str(parameter.annotation)

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
        event_type = str(type(event))

        if event_type not in self._consumers:
            return

        consumer_group = self._consumers[event_type]

        for consumer in consumer_group:
            consumer.process(event)
