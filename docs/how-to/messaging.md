# How to: Messaging & Event Distribution

The Shared Kernel provides two main mechanisms for event distribution: the **Event Broker** for in-memory pub-sub with domain event handlers, and the **Event Dispatcher** for projection-based scenarios.

## 1. Using the Event Broker

The `EventBroker` is used to notify `DomainEventHandler` subscribers when an infrastructure event is received. It converts raw events into domain events using a `MappingPipeline` and automatically propagates the event's correlation ID through the request context, ensuring `get_request_id()` returns the correct value inside handlers.

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
from sharedkernel.infrastructure.data import Event
from sharedkernel.infrastructure.mappers import MappingPipeline
from sharedkernel.infrastructure.services import EventBroker
import logging

logger = logging.getLogger(__name__)

# The broker needs a mapper to convert raw events to domain events
mapper = MappingPipeline()
# ... register mapping behaviors ...

broker = EventBroker(logger, mapper)

# Subscribe the handler
handler = WelcomeEmailHandler()
broker.subscribe(handler)

# Publish a raw infrastructure event
raw_event = Event(event_type="UserRegistered", data='{"email": "john@example.com"}', ...)
broker.publish(raw_event)
```

---

## 2. Using the Event Dispatcher

The `EventDispatcher` is used to route infrastructure events to `Projector` subscribers that build and maintain read models. It converts raw events into domain events using a `MappingPipeline` and passes the aggregate's `stream_id` to each projector so it can track positions per entity.

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

---

## 3. Event Broker vs Event Dispatcher

Both services accept raw `Event` objects and use a `MappingPipeline` to convert them into domain events, but they serve different purposes and target different subscriber types.

| | Event Broker | Event Dispatcher |
|---|---|---|
| **Purpose** | Execute side effects and business reactions (sagas) | Build and maintain read models (projections) |
| **Subscribers** | `DomainEventHandler[TEvent]` | `Projector[TProjection]` |
| **Correlation ID** | Propagates `event.correlation_id` via `set_request_id()` so downstream handlers and repositories can correlate events back to the originating request | Does not manage request context |
| **Position tracking** | Passes `event.position` to handlers | Passes `event.position` and `event.stream_id` to projectors, enabling per-entity position tracking and idempotent replay |
| **Mapper not found** | Logs a warning and skips | Raises `MapperNotFound` |

### When to use the Event Broker

Use the `EventBroker` when consuming events triggers **write-side operations** — commands on other aggregates, integration messages, or saga orchestration. The broker ensures the correlation chain is preserved so that events produced by secondary aggregates can be traced back to the original request.

Typical consumers: Kafka event consumers that feed saga handlers.

### When to use the Event Dispatcher

Use the `EventDispatcher` when consuming events updates **read-side projections** — denormalized views optimized for queries. The dispatcher passes the `stream_id` to projectors so they can track which events have been applied per entity, enabling idempotent replay and ordered processing.

Typical consumers: Event store catch-up subscriptions that feed projectors.
