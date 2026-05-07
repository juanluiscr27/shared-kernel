# Errors and Exceptions

The Shared Kernel separates two concepts: **exceptions** (raised at runtime to interrupt control flow) live in `exceptions.py` modules, while **error data classes** (value objects passed around as data) live in `errors.py` modules.

## Exceptions

### Base Exceptions

- **`SystemException`**: Base class for all exceptions in the system (`domain/exceptions.py`).
- **`DomainException`**: Raised when a business rule is violated. It captures the aggregate involved and a human-readable message (`domain/exceptions.py`).
- **`ApplicationException`**: Raised during the orchestration of business logic, e.g., in the Service Bus (`application/exceptions.py`).
- **`InfrastructureException`**: Raised during interaction with external services (`infrastructure/exceptions.py`).
- **`ApiException`**: Raised when processing requests or returning responses (`api/exceptions.py`).

### Domain Exceptions

- **`UnhandledEventType`**: Raised when an aggregate or projection receives an event it doesn't know how to handle.
- **`EntityNotFound`**: Raised when an entity cannot be found in a repository or aggregate.
- **`InvalidState`**: Raised when an entity's state is invalid for the requested operation (business rule violated).
- **`UniqueConstraintViolation`**: Raised when a unique constraint on an identity value is violated.
- **`ConcurrencyConflict`**: Raised when an entity has been modified by another transaction since it was read (optimistic concurrency).

### Application Exceptions

- **`HandlerAlreadyRegistered`**: Raised when trying to register a handler for a request type that already has one.
- **`UnsupportedHandler`**: Raised when trying to register an invalid handler type in the `ServiceBus`.

### Infrastructure Exceptions

- **`EventOutOfSequence`**: Raised by a `Projector` when it receives an event with a position that doesn't match the expected sequence.
- **`MapperNotFound`**: Raised when the `MappingPipeline` cannot find a mapper for a specific event type.
- **`UnsupportedEventHandler`**: Raised when trying to subscribe an invalid handler to the `EventBroker`.
- **`UnprocessableListener`**: Raised when a listener cannot be processed because it handles zero event types.
- **`IntegrityError`**: Raised on optimistic concurrency control failures in the infrastructure layer.

## Error Data Classes

- **`Error`**: A frozen dataclass used to pass error information as data, common in validation results and service bus internal errors (`domain/errors.py`).
- **`ErrorDetail`**: A machine-readable error detail for HTTP responses (`application/errors.py`).
- **`Rejection`**: A standardized object returned by the `ServiceBus` when a request cannot be processed, e.g., due to validation errors or domain exceptions (`application/errors.py`).
- **`ServiceBusErrors`**: A catalog of `Error` factory methods for common service bus failures (`application/errors.py`).

## Best Practices

1. **Use Exceptions**: Raise `DomainException` subclasses from handlers for expected business failures. The `ServiceBus` catches and converts them to `Rejection` responses with appropriate HTTP status codes. It also catches `ValueError` exceptions (e.g., from `Guard` clauses) and maps them to `Rejection` with a 422 status code.
2. **Standardize Domains**: Use the `domain` field in the `Error` object to specify where the error originated (e.g., "Users", "Billing").
3. **Capture Context**: When raising a `DomainException`, always pass the source instance and provide a meaningful `code` and `reason` for consistent API error responses.
