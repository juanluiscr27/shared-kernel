# DDD Concepts in Shared Kernel

This page explains how classic Domain-Driven Design (DDD) concepts map to the classes in this library.

## Strategic Patterns: The Shared Kernel

A **Shared Kernel** is one of the ways distinct Bounded Contexts can relate to each other. It represents a small, shared subset of the domain model that two or more teams agree to keep in sync. By using this library, you are standardizing this "kernel" to facilitate easier integration between your services.

## Tactical Patterns

### Aggregates
The primary unit of encapsulation in DDD. In this library, the `Aggregate` class provides:
- **Versioning**: For optimistic concurrency control.
- **Event Tracking**: An internal queue (`_events`) to record what happened during a transaction.
- **Root Entity Identity**: Every aggregate has a root entity with a strongly typed `EntityID`.

### Entities
Objects defined by their identity. Even if all other attributes are the same, two entities with different IDs are different.
- Implementation: `sharedkernel.domain.models.Entity`.

### Value Objects
Objects defined by their attributes. Two value objects with the same attributes are considered equal.
- Implementation: `sharedkernel.domain.models.ValueObject`.
- Tip: Use `@dataclass(frozen=True)` to ensure immutability.

### Domain Events
Something that happened in the domain that domain experts care about.
- Implementation: `sharedkernel.domain.events.DomainEvent`.
- Lifecycle: Raised by an `Aggregate` -> Handled by a `DomainEventHandler`.

### Repositories
An abstraction for a collection of aggregates. It hides the details of the underlying storage.
- Implementation: `sharedkernel.domain.repositories.Repository`.

### Domain Services
Logic that doesn't naturally belong to a single entity or aggregate.
- Implementation: `sharedkernel.domain.services.DomainService`.

## Why use this library?

1. **consistency**: Ensure every context uses the same base logic for CQRS and DDD.
2. **Speed**: Stop reinventing the wheel (Service Bus, Event Broker, Projectors).
3. **Safety**: Leverage the built-in `Guard` and `Detect` classes to ensure domain integrity and security.
