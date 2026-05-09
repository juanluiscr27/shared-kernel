# How to: Persistence & Event Sourcing

The Shared Kernel provides abstract interfaces for data access, allowing your domain to remain independent of specific database technologies.

## 1. Using Repositories

**Repositories** are responsible for persisting and retrieving aggregate roots. The `Repository` interface supports two unit-of-work persistence methods:

- **`save(entity)`** — Persists the entity and **commits** the transaction immediately.
- **`add(entity)`** — Stores the entity but **leaves the transaction open**, allowing the caller to coordinate multiple operations within a single unit of work before committing.

Use `save` for simple, self-contained operations. Use `add` when you need to persist multiple aggregates or coordinate with an event store within the same transaction.

### Define the Repository Interface

In your **Domain** or **Application** layer:

```python
from sharedkernel.domain.repositories import Repository
from mydomain.models import User

class UserRepository(Repository[User]):
    # Note: Define your abstract methods here
    pass
```

### Implement the Repository

In your **Infrastructure** layer:

```python
class SqlAlchemyUserRepository(UserRepository):
    def save(self, user: User):
        # Persists the entity and commits the transaction
        pass

    def add(self, user: User):
        # Stores the entity without committing (unit-of-work)
        pass

    def find_by_id(self, user_id: UserID) -> User:
        # Concrete implementation...
        pass
```

---

## 2. Using the Event Store

If you are using **Event Sourcing**, you store individual events instead of the aggregate's current state.

### The Event Store Interface

The `EventStore` interface defines an append-only log of events with two unit-of-work persistence methods:

- **`stage(stream_id, events, ...)`** — Stages events to a stream **without committing** the transaction. If a concurrency conflict is detected, the transaction is rolled back and `-1` is returned. Use this when you need to coordinate event persistence with other operations within a single unit of work.
- **`append(stream_id, events, ...)`** — Appends events to a stream and **commits** the transaction if there is no conflict. Use this for self-contained operations where no further coordination is needed.

```python
from sharedkernel.infrastructure.database import EventStore
from sharedkernel.infrastructure.data import Event

class MyEventStore(EventStore[Event, Stream]):
    def stage(self, stream_id, events, ...):
        # Stage events without committing (unit-of-work)...
        pass

    def append(self, stream_id, events, ...):
        # Append events and commit the transaction...
        pass

    def get_all(self, stream_id, from_version):
        # Replay events from your database...
        pass
```

---

## 3. Projections & Read Models

In CQRS, **Read Models** are optimized for data retrieval and are often distinct from the write models.

### Defining a Data Model

Use `DataModel` (infrastructure level) or `ReadModel` (application level) for your DTOs.

```python
from sharedkernel.infrastructure.data import DataModel
from dataclasses import dataclass

@dataclass(frozen=True)
class UserSummary(DataModel):
    user_id: int
    name: str
```

### Building Projections

See the [Messaging How-to](messaging.md) for details on using the `Projector` and `EventDispatcher` to keep your read models in sync with your write models.
