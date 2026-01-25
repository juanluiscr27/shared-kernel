# Error Catalog

The Shared Kernel provides a hierarchy of exceptions to help you distinguish between different types of failures.

## Base Exceptions

- **`DomainException`**: Raised when a business rule is violated. It captures the aggregate involved and a human-readable message.
- **`SystemException`**: Base class for technical failures.
- **`ApplicationException`**: Raised during the orchestration of business logic (e.g., in the Service Bus).

## Common Domain Errors

- **`UnknownEvent`**: Raised when an aggregate or projection receives an event it doesn't know how to handle.
- **`Error`**: A simple DTO used to pass error information without raising exceptions (common in `Result` objects).

## Application Errors

- **`HandlerAlreadyRegistered`**: Raised when trying to register a handler for a request type that already has one.
- **`UnsupportedHandler`**: Raised when trying to register an invalid handler type in the `ServiceBus`.
- **`Rejection`**: A standardized object returned by the `ServiceBus` when a request cannot be processed (e.g., due to validation errors).

## Infrastructure Errors

- **`OutOfOrderEvent`**: Raised by a `Projector` when it receives an event with a position that doesn't match the expected sequence.
- **`MapperNotFound`**: Raised when the `MappingPipeline` cannot find a mapper for a specific event type.
- **`UnsupportedEventHandler`**: Raised when trying to subscribe an invalid handler to the `EventBroker`.

## Best Practices

1. **Use `Result`**: Favor returning `Result[T, Error]` from your handlers instead of raising exceptions for expected business failures.
2. **Standardize Domains**: Use the `domain` field in the `Error` object to specify where the error originated (e.g., "Users", "Billing").
3. **Capture Context**: When raising a `DomainException`, always pass the aggregate instance so the system can log the full context.
