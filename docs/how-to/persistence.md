# How to: Persistence & Event Sourcing

The Shared Kernel provides abstract interfaces for data access, allowing your domain to remain independent of specific database technologies.

## 1. Using Repositories

**Repositories** are responsible for persisting and retrieving aggregate roots.

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
        # Concrete implementation using SQLAlchemy...
        pass

    def find_by_id(self, user_id: UserID) -> User:
        # Concrete implementation...
        pass
```

---

## 2. Using the Event Store

If you are using **Event Sourcing**, you store individual events instead of the aggregate's current state.

### The Event Store Interface

The `EventStore` interface defines an append-only log of events.

```python
from sharedkernel.infrastructure.database import EventStore
from sharedkernel.infrastructure.data import Event

class MyEventStore(EventStore[Event, Stream]):
    def append(self, stream_id, events, ...):
        # Append events to your database...
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
