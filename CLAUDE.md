# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Shared Kernel is a Python 3.12+ library implementing the Shared Kernel pattern for Domain-Driven Design (DDD) and Clean Architecture. It provides base classes and infrastructure for building microservices with CQRS, Event Sourcing, and strict layered architecture.

**Key dependencies:** Pydantic 2.12.5+, typeinspection (custom git dep for generic type introspection).

## Common Commands

```bash
# Install dependencies
uv sync

# Run all tests
uv run tox -e py312

# Run a single test file
uv run pytest tests/domain/test_models.py

# Run a single test by name
uv run pytest -k "test_name"

# Run tests with coverage
uv run tox -e py312 && uv run tox -e coverage

# Lint
uv run ruff check .

# Type check
uv run mypy sharedkernel/
```

## Architecture

The library enforces Clean Architecture with four layers. Dependencies point inward (API → Application → Domain ← Infrastructure):

- **Domain** (`sharedkernel/domain/`): Pure business logic — ValueObject, Entity, Aggregate, DomainEvent, Guard clauses, Repository interfaces, domain exceptions and errors
- **Application** (`sharedkernel/application/`): CQRS orchestration — Command/Query handlers, ServiceBus (request router), Validators, RequestContext with contextvars
- **Infrastructure** (`sharedkernel/infrastructure/`): Technical implementations — EventBroker (in-memory pub-sub), EventDispatcher, MappingPipeline, EventStore interface, JSON encoders
- **API** (`sharedkernel/api/`): External contracts — Pydantic-based Request/Response models, ProblemDetail error responses, AckResponse

### Key Patterns

- **Exceptions vs Errors:** Exception classes (raised at runtime) live in `exceptions.py` per layer; error data classes (value objects) live in `errors.py`. Each layer has its own base exception (`DomainException`, `ApplicationException`, `InfrastructureException`, `ApiException`) inheriting from `SystemException`.
- **Exception-based handlers:** Handlers return values directly (`Acknowledgement` or `ReadModel | ReadModelList`) and raise `DomainException` subclasses for business rule violations. The `ServiceBus` catches exceptions and converts them to `Rejection` responses.
- **Frozen dataclasses:** ValueObjects and DomainEvents use `@dataclass(frozen=True)` for immutability.
- **Generic handlers:** `CommandHandler[TCommand]`, `QueryHandler[TQuery]`, `Validator[TRequest]` — the ServiceBus uses type introspection on generic parameters for routing.
- **ServiceBus:** Uses separate `_command_handlers` and `_query_handlers` dicts for correct type narrowing. Type aliases `Handler`, `Request`, `Response` are defined in `application/services.py`.
- **Aggregates:** Track domain events via `_events` deque, expose `.changes`, use `_raise_event()` to apply and record events. Support optimistic concurrency via `version` field.
- **Guard clauses:** Static methods on `Guard` class for fail-fast validation in constructors/factory methods.

## Code Conventions

- Strict mypy: `disallow_untyped_defs`, `disallow_any_generics`, full type annotations required
- Ruff linting with broad rule set (E, W, I, N, D, UP, B, C4, SIM, RET, TRY, RSE, ARG, PTH, PL, S, ANN, RUF)
- Google docstring convention (`lint.pydocstyle.convention = "google"` in `ruff.toml`)
- Max line length: 120
- Tests mirror source structure under `tests/`; test files have relaxed lint rules (no docstrings, annotations, or assert warnings)
- All generic classes must have explicit type parameters (use `[Any]` when accepting any variant)
