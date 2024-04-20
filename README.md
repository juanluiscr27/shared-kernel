# Shared Kernel

[![Build Status](https://github.com/juanluiscr27/shared-kernel/actions/workflows/tests.yaml/badge.svg)](https://github.com/juanluiscr27/shared-kernel/actions) 
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://docs.python.org/3.12/index.html) 
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/) 

A Python library that implements a Shared Kernel pattern for projects built using Domain-Driven Design principles.

## Features

A Shared Kernel is a relationship in DDD where two or more bounded contexts share common elements.
The catalog of elements included in this libray are as follows:

* Value Objects, Domain Entities, Aggregates
* Domain Service
* CQRS Pattern with Commands, Queries and Handlers
* Domain Events and Event Handlers
* Guard Clauses
* Command Validator
* Domain Errors
* Event Broker (in memory)
* Repository Pattern
* API Contracts
* Clean Architecture

### Dependencies

Shared Kernel is built using Python 3.12 and depends on the follow libraries:
* [Pydantic](https://github.com/pydantic/pydantic)
* [Result](https://github.com/rustedpy/result)

## Quick Start

### Installation

To install Share Kernel using pip, just run:

```shell
pip install git+https://github.com/juanluiscr27/shared-kernel.git@v0.1.0-beta#egg=sharedkernel
```
## Usage

Shared Kernel is ease to use, here we have some examples.

### Value Objects

Define two value object with same value. They both should be equal.

```python
from dataclasses import dataclass

from sharedkernel.domain import ValueObject


@dataclass(frozen=True)
class Money(ValueObject):
    amount: float = 0
    currency: str = "USD"


# creating two money objects with same amount and currency value
expected = Money(10, "CAD")

result = Money(10, "CAD")

assert result == expected
```

### Domain Entities

Define two entities with same ids and they both should be equal.

```python
from dataclasses import dataclass

from sharedkernel.domain import Entity, EntityID


@dataclass(frozen=True)
class CountryID(EntityID):
    value: str


class Country(Entity[CountryID]):

    def __init__(self, country_id: CountryID, name: str):
        super().__init__(country_id)
        self.name = name


# defining a strongly typed id for our entities 
do = CountryID("DO")

dr = Country(country_id=do, name="Dominican Rep.")

dom_rep = Country(country_id=do, name="Dominican Republic")

assert dr == dom_rep
```

### Guard Clauses

A guard clause is a software pattern that promote "failing fast".  
Here we are checking if an email is null or empty and throw a `ValueError` if any are found.

```python
from dataclasses import dataclass

from sharedkernel.domain import ValueObject
from sharedkernel.domain.services import Guard


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str):
        Guard.is_not_null_or_empty(value)
        return cls(value)


# defining an empty email
empty_email = ""

try:
    _ = Email.create(empty_email)
except ValueError as error:
    print(error)  # Email cannot be null nor empty
```
