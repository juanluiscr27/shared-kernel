# Getting Started

This tutorial will guide you through the basic steps of using the **Shared Kernel** library to define a simple domain model and handle a command.

## 1. Prerequisites

Ensure you have Python 3.12+ installed.

```bash
pip install sharedkernel
```

## 2. Define your Domain Model

Let's start by defining a simple `User` aggregate. In DDD, an **Aggregate** is a cluster of domain objects that can be treated as a single unit.

### Define an Entity ID

We use strongly typed IDs to avoid "primitive obsession".

```python
from dataclasses import dataclass
from uuid import UUID
from sharedkernel.domain.models import EntityID

@dataclass(frozen=True)
class UserID(EntityID):
    value: UUID
```

### Define a Value Object

Value objects are immutable and defined by their attributes rather than a unique identity.

```python
from dataclasses import dataclass
from sharedkernel.domain.models import ValueObject

@dataclass(frozen=True)
class Email(ValueObject):
    address: str
```

### Define the Aggregate Root

The aggregate root is responsible for enforcing business rules.

from sharedkernel.domain.models import Aggregate

```python
class User(Aggregate[UserID]):
    def __init__(self, user_id: UserID, version: int, state: UserState):
        super().__init__(user_id, version)
        self._state: state

    @classmethod
    def load(cls, user_id: UserID, version: int, state: UserState, events: tuple):
        user = cls(user_id=user_id, version=version, state=state)

        for event in events:
            user._apply(event)

        return user

    @classmethod
    def register(cls, user_id: UserID, name: str, email: Email):
        user = cls(user_id=user_id, version=0, state=UserState.default())

        user_registered = UserRegistered(user_id=user_id.value, name=name, email=email.address)

        user._raise_event(user_registered)

        return user

    @singledispatchmethod
    def _apply(self, event: DomainEvent) -> None:
        super()._apply(event)

    @_apply.register
    def _when(self, event: UserRegistered) -> None:
        self.state = UserState(name=event.name, email=event.email)
```

## 3. Handle a Command

Now let's see how to register a user using the **Service Bus**.

### Define a Command

```python
from dataclasses import dataclass
from uuid import UUID
from sharedkernel.application.commands import Command

@dataclass(frozen=True)
class RegisterUser(Command):
    user_id: UUID
    name: str
    email: str
```

### Create a Command Handler

```python
from result import Result, Ok
from sharedkernel.application.commands import CommandHandler, Acknowledgement, CommandStatus
from sharedkernel.domain.errors import Error

class RegisterUserHandler(CommandHandler[RegisterUser]):
    def execute(self, command: RegisterUser) -> Result[Acknowledgement, Error]:
        # Business logic goes here...
        
        ack = Acknowledgement(
            status=CommandStatus.RECEIVED,
            action=type(command).__name__,
            entity_id=command.user_id,
            version=1
        )
        return Ok(ack)
```

### Dispatch via Service Bus

```python
import logging
from sharedkernel.application.services import ServiceBus, RequestContext

# Initialize the bus
logger = logging.getLogger(__name__)
bus = ServiceBus(logger)

# Register the handler
bus.register(RegisterUserHandler())

# Send the command
command = RegisterUser(user_id=UUID('...'), name="John Doe", email="john@example.com")
context = RequestContext.new(request_id=UUID('...'), timestamp=None)

response = bus.send(command, context)
print(f"User registration status: {response.status}")
```

## Next Steps

- Learn more about [Domain Models](../how-to/domain-models.md).
- Explore [Messaging and the Service Bus](../how-to/messaging.md).
- Understand the [Architecture Overview](../explanation/architecture.md).
