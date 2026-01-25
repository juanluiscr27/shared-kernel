# How to: Implement Validation

The Shared Kernel provides multiple levels of validation: low-level **Guards** for domain invariants and high-level **Validators** for application requests.

## 1. Domain Guards

**Guards** promote the "Fail-Fast Principle". They are typically used inside value object creation or entity methods.

### Available Guards

The `sharedkernel.domain.services.Guard` class includes:
- `is_not_null(value)`
- `is_not_empty(value)`
- `is_not_null_or_empty(value)`
- `minimum_length(value, length)`
- `maximum_length(value, length)`
- `is_greater_than(value, min)`
- `is_less_than(value, max)`

### Example usage

```python
from sharedkernel.domain.services import Guard

class Product:
    def __init__(self, name: str, price: float):
        Guard.is_not_null_or_empty(name)
        Guard.is_greater_than(price, 0)
        self.name = name
        self.price = price
```

---

## 2. Request Validators

**Validators** are used in the application layer to validate `Commands` or `Queries` before they are processed by a handler.

### Defining a Validator

Implement the `Validator[TRequest]` interface.

```python
from sharedkernel.application.validators import Validator, ValidationResult
from sharedkernel.domain.errors import Error

class RegisterUserValidator(Validator[RegisterUser]):
    def validate(self, request: RegisterUser) -> ValidationResult:
        errors = []
        
        if len(request.name) < 3:
            errors.append(Error(
                message="Name too short",
                code="User.Name.TooShort",
                domain="Users"
            ))
            
        if errors:
            return ValidationResult.with_errors(errors)
            
        return ValidationResult.success()
```

### Registering with the Service Bus

When you register a validator in the `ServiceBus`, it is automatically executed before the corresponding handler.

```python
bus = ServiceBus(logger)
bus.register(RegisterUserHandler())
bus.register(RegisterUserValidator()) # This will run before RegisterUserHandler
```

## 3. SQL Injection Detection

The `Detect` class provides utility methods to identify common SQL injection patterns.

```python
from sharedkernel.domain.services import Detect

def search(query: str):
    Detect.special_character(query) # Raises ValueError if '"', ';', '--', etc. are found
    Detect.reserved_word(query)    # Raises ValueError if 'SELECT', 'DROP', etc. are found
    # ... execute search
```
