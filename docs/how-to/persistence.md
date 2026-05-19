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

## 3. Query Specifications

**Query Specifications** let you build type-safe, composable query predicates for filtering, sorting, and paginating read models. They produce database-agnostic expressions that your infrastructure layer translates into actual queries.

### Building Conditions

Use the `Condition` factory methods to create filter predicates:

```python
from sharedkernel.domain.specifications import Condition

# Comparison filters
Condition.equal(field_name='country', value='DO')
Condition.not_equal(field_name='status', value='inactive')
Condition.greater_than(field_name='points', value=20)
Condition.less_than_or_equal(field_name='weight', value=95.5)

# Pattern matching
Condition.contains(field_name='last_name', value='garcia')
Condition.starts_with(field_name='slug', value='garcia')
Condition.ends_with(field_name='slug', value='jr')

# Range and membership
Condition.between(field_name='year', left=2024, right=2026)
Condition.is_in(field_name='country', values=['DO', 'US', 'PR'])

# Null checks
Condition.is_null(field_name='description')
Condition.is_not_null(field_name='headshot_url')
```

### Combining with Predicate Groups

Use `PredicateGroup` to combine conditions with `AND` / `OR` logic, and the `|` and `&` operators to compose groups:

```python
from sharedkernel.domain.specifications import PredicateGroup, LogicalOperator

# Simple AND group
predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
    Condition.equal(field_name='country', value='DO'),
    Condition.equal(field_name='status', value='active'),
])

# Composing OR with AND
position_filter = PredicateGroup(operator=LogicalOperator.OR, predicates=[
    Condition.equal(field_name='position', value='PG'),
])
stats_filter = PredicateGroup(operator=LogicalOperator.AND, predicates=[
    Condition.greater_than(field_name='pts', value=20),
    Condition.greater_than(field_name='ast', value=10),
])

predicate = position_filter | stats_filter
# Produces: (position = 'PG') OR (pts > 20 AND ast > 10)
```

### Full Query Specification

Combine predicates with sorting and pagination into a `QuerySpecification`:

```python
from sharedkernel.domain.specifications import (
    Condition, PredicateGroup, LogicalOperator,
    SortOrder, SortDirection, Pagination, QuerySpecification,
)

predicate = Condition.equal(field_name='country', value='DO')
sorting = [SortOrder(field_name='last_name', direction=SortDirection.ASC)]
pagination = Pagination(limit=10, offset=0)

specification = QuerySpecification(
    predicate=predicate,
    sorting=sorting,
    pagination=pagination,
)

specification.to_expression()
# "WHERE country = 'DO' ORDER BY last_name ASC LIMIT 10 OFFSET 0"
```

Your repository implementations can accept a `QuerySpecification` and translate it into the appropriate database query.

---

## 4. Projections & Read Models

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
