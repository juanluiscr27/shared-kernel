# Shared Kernel

Welcome to the **Shared Kernel** documentation. This library provides a robust foundation for building Python applications following **Domain-Driven Design (DDD)**, **CQRS**, and **Clean Architecture** patterns.

## What is a Shared Kernel?

In Domain-Driven Design, a **Shared Kernel** is a relationship where two or more bounded contexts share a common set of elements. This library provides those common elements to ensure consistency across your microservices or modules while maintaining clean boundaries.

## Key Features

- **DDD Primitives**: `ValueObject`, `Entity`, `Aggregate`, `EntityID`.
- **CQRS Infrastructure**: `Command`, `Query`, `CommandHandler`, `QueryHandler`.
- **Messaging**: A high-performance `ServiceBus` for dispatching requests.
- **Event Sourcing & Projections**: Tools for managing event streams and building read models.
- **Validation & Guards**: "Fail-fast" validation mechanisms for robust domain models.
- **API Contracts**: Standardized request/response structures using Pydantic.

## Quick Start

### Installation

```bash
pip install git+https://github.com/juanluiscr27/shared-kernel.git@v4.0.0-beta#egg=sharedkernel
```

### Basic Example: Value Objects

```python
from dataclasses import dataclass
from sharedkernel.domain.models import ValueObject

@dataclass(frozen=True)
class Money(ValueObject):
    amount: float
    currency: str = "USD"

# Equality is based on value, not identity
price1 = Money(100)
price2 = Money(100)
assert price1 == price2
```

## Navigation

- [**Tutorials**](tutorials/getting-started.md): Get up and running in minutes.
- [**How-to Guides**](how-to/messaging.md): Practical recipes for common tasks.
- [**API Reference**](reference/api.md): Detailed technical documentation.
- [**Concepts**](explanation/architecture.md): Deep dives into the library's design.
