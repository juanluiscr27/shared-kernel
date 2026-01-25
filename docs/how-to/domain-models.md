# How to: Implement Domain Models

This guide explains how to use the base classes provided by the Shared Kernel to build your domain model.

## Value Objects

**Value Objects** are immutable objects that have no identity. Their equality is determined by their properties.

### Basic Implementation

```python
from dataclasses import dataclass
from sharedkernel.domain.models import ValueObject

@dataclass(frozen=True)
class Address(ValueObject):
    street: str
    city: str
    zip_code: str
```

### Adding Logic

You can add methods to value objects, but they must return new instances to maintain immutability.

```python
@dataclass(frozen=True)
class Money(ValueObject):
    amount: float
    currency: str = "USD"
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Currencies do not match")
        return Money(self.amount + other.amount, self.currency)
```

---

## Entities

**Entities** are objects with a unique identity that persists over time.

```python
from sharedkernel.domain.models import Entity, EntityID
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ProductID(EntityID):
    value: UUID

class Product(Entity[ProductID]):
    def __init__(self, product_id: ProductID, name: str, price: float):
        super().__init__(product_id)
        self.name = name
        self.price = price
```

---

## Aggregates

An **Aggregate** is a group of entities and value objects treated as a single consistency boundary. The **Aggregate Root** (the main entity) is responsible for managing its state and raising events.

### Raising Domain Events

Aggregates can record events that happen within them.

```python
from dataclasses import dataclass
from sharedkernel.domain.events import DomainEvent
from sharedkernel.domain.models import Aggregate

@dataclass(frozen=True)
class PriceChanged(DomainEvent):
    product_id: UUID
    new_price: float

class ProductAggregate(Aggregate[ProductID]):
    def __init__(self, product_id: ProductID, version: int, name: str, price: float):
        super().__init__(product_id, version)
        self.name = name
        self.price = price

    def update_price(self, new_price: float):
        self.price = new_price
        # Record the event
        self._raise_event(PriceChanged(product_id=self.id.value, new_price=new_price))
```

### Applying Events (Event Sourcing)

If you use event sourcing, your aggregate should know how to apply events to reconstruct its state.

```python
from functools import singledispatchmethod

class User(Aggregate[UserID]):
    def __init__(self, user_id: UserID, version: int, name: str):
        super().__init__(user_id, version)
        self.name = name

    @singledispatchmethod
    def _apply(self, event: DomainEvent) -> None:
        super()._apply(event)

    @_apply.register
    def _when_registered(self, event: UserRegistered) -> None:
        self.name = event.name
```

---

## Using Guards

Always use the `Guard` class in your constructors or factory methods to ensure your domain models are always in a valid state.

```python
from sharedkernel.domain.services import Guard

class Email(ValueObject):
    @classmethod
    def create(cls, address: str):
        Guard.is_not_null_or_empty(address)
        # Add custom email regex validation here...
        return cls(address)
```
