# My First Aggregate

This tutorial will show you how to build a complete Aggregate Root with ID, attributes, and domain events.

## 1. Define the Identity

Every aggregate must have a unique, strongly-typed identity.

```python
from dataclasses import dataclass
from uuid import UUID
from sharedkernel.domain.models import EntityID

@dataclass(frozen=True)
class OrderID(EntityID):
    value: UUID
```

## 2. Define the Domain Events

Aggregates communicate changes via events.

```python
from dataclasses import dataclass
from sharedkernel.domain.events import DomainEvent

@dataclass(frozen=True)
class OrderCreated(DomainEvent):
    order_id: UUID
    customer_id: UUID
```

## 3. Create the Aggregate Root

Extend `Aggregate[TId]`. Use `_raise_event` to record changes.

```python
from sharedkernel.domain.models import Aggregate

class Order(Aggregate[OrderID]):
    def __init__(self, order_id: OrderID, version: int, customer_id: UUID):
        super().__init__(order_id, version)
        self.customer_id = customer_id
        self.items = []

    @classmethod
    def create(cls, order_id: OrderID, customer_id: UUID):
        # 1. Instantiate
        order = cls(order_id, version=0, customer_id=customer_id)
        
        # 2. Raise event
        order._raise_event(OrderCreated(order_id.value, customer_id))
        
        return order
```

## 4. Why use `_raise_event`?

When you call `_raise_event(event)`:
1. The aggregate's `_apply(event)` method is called (ideal for event sourcing).
2. The event is added to the `changes` collection.
3. This collection can later be persisted to an `EventStore`.

## 5. Cleaning up

After the aggregate has been saved, you should clear its internal events to prevent duplicate processing.

```python
order.clear_events()
assert len(order.changes) == 0
```
