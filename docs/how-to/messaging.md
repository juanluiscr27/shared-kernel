# How to: Messaging & Event Distribution

The Shared Kernel provides two main mechanisms for event distribution: the **Event Broker** for simple in-memory pub-sub, and the **Event Dispatcher** for complex scenarios like projections and mapping raw events to domain events.

## 1. Using the Event Broker (In-Memory)

The `EventBroker` is used to notify internal subscribers when a domain event occurs within the same process.

### Define an Event Handler

Implement the `DomainEventHandler[TEvent]` interface.

```python
from sharedkernel.domain.events import DomainEventHandler
from mydomain.events import UserRegistered

class WelcomeEmailHandler(DomainEventHandler[UserRegistered]):
    def process(self, event: UserRegistered, position: int):
        print(f"Sending welcome email to {event.email}")
```

### Subscribe and Publish

```python
from sharedkernel.infrastructure.services import EventBroker
import logging

logger = logging.getLogger(__name__)
broker = EventBroker(logger)

# Subscribe the handler
handler = WelcomeEmailHandler()
broker.subscribe(handler)

# Publish an event
event = UserRegistered(email="john@example.com")
broker.publish(event, position=1)
```

---

## 2. Using the Event Dispatcher (Projections)

The `EventDispatcher` is more specialized. It works with a `MappingPipeline` to convert raw infrastructure events into domain events and passes them to `Projectors`.

### Define a Projector

A `Projector` wraps a `Projection` and handles common logic like ensuring events are processed in order.

```python
from sharedkernel.infrastructure.projections import Projector, Projection
from sharedkernel.domain.events import DomainEvent
from mydomain.read_models import UserModel

class UserDetailsProjection(Projection[UserModel]):
    def get_position(self, entity_id, event_type):
        # Retrieve current position from database...
        return 0

    def apply(self, event: DomainEvent):
        # Update your read model...
        pass

    def update_position(self, entity_id, event_type, position):
        # Save new position to database...
        pass
```

### Subscribe and Dispatch

```python
from sharedkernel.infrastructure.services import EventDispatcher
from sharedkernel.infrastructure.mappers import MappingPipeline

# The dispatcher needs a mapper to understand raw events
mapper = MappingPipeline()
# ... register mappers ...

dispatcher = EventDispatcher(logger, mapper)

# Register the projector
projector = Projector(logger, UserDetailsProjection())
dispatcher.subscribe(projector)

# Dispatch a raw infrastructure event
raw_event = Event(event_type="UserRegistered", data='{"email": "..."}', ...)
dispatcher.dispatch(raw_event)
```
