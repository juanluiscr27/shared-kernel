from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import StrEnum
from typing import Sequence
from uuid import UUID


class LogicalOperator(StrEnum):
    AND = "AND"
    OR = "OR"


class Predicate(ABC):

    @abstractmethod
    def to_expression(self) -> str:
        pass


class Filter(Predicate):

    def __init__(self, field_name: str):
        self._field_name = field_name

    @property
    def field_name(self) -> str:
        return self._field_name

    def to_expression(self) -> str:
        pass


DataValue = str | int | float | bool | datetime | UUID


def format_value(value: DataValue) -> str:
    if isinstance(value, str):
        return f"'{value}'"

    if isinstance(value, bool):
        return str(value).upper()

    if isinstance(value, datetime):
        return f"'{value.isoformat()}'"

    if isinstance(value, UUID):
        return f"'{value}'"

    return str(value)


def format_iterable(values: Sequence[DataValue]) -> str:
    formatted = ", ".join(format_value(value) for value in values)

    return f"({formatted})"


class EqualFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} = {self.value}"


class NotEqualFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} != {self.value}"


class LessThanFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} < {self.value}"


class LessThanOrEqualFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} <= {self.value}"


class GreaterThanFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} > {self.value}"


class GreaterThanOrEqualFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} >= {self.value}"


class InFilter(Filter):
    def __init__(self, field_name: str, values: Sequence[DataValue]):
        super().__init__(field_name)
        self._values = format_iterable(values)

    @property
    def values(self) -> DataValue:
        return self._values

    def to_expression(self) -> str:
        return f"{self.field_name} IN {self.values}"


class NotInFilter(Filter):
    def __init__(self, field_name: str, values: Sequence[DataValue]):
        super().__init__(field_name)
        self._values = format_iterable(values)

    @property
    def values(self) -> DataValue:
        return self._values

    def to_expression(self) -> str:
        return f"{self.field_name} NOT IN {self.values}"


class BetweenFilter(Filter):
    def __init__(self, field_name: str, left: DataValue, right: DataValue):
        super().__init__(field_name)
        self._left_value = format_value(left)
        self._right_value = format_value(right)

    @property
    def left(self) -> DataValue:
        return self._left_value

    @property
    def right(self) -> DataValue:
        return self._right_value

    def to_expression(self) -> str:
        return f"{self.field_name} BETWEEN {self.left} AND {self.right}"


class ContainsFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} LIKE '%{self._raw_value}%'"


class NotContainsFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} NOT LIKE '%{self._raw_value}%'"


class StartsWithFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} LIKE '{self._raw_value}%'"


class EndsWithFilter(Filter):
    def __init__(self, field_name: str, value: DataValue):
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> DataValue:
        return self._value

    def to_expression(self) -> str:
        return f"{self.field_name} LIKE '%{self._raw_value}'"


class IsNullFilter(Filter):
    def __init__(self, field_name: str):
        super().__init__(field_name)

    def to_expression(self) -> str:
        return f"{self.field_name} IS NULL"


class IsNotNullFilter(Filter):
    def __init__(self, field_name: str):
        super().__init__(field_name)

    def to_expression(self) -> str:
        return f"{self.field_name} IS NOT NULL"


class Condition(Predicate):

    def __init__(self, predicate_filter: Filter):
        self._filter = predicate_filter

    def to_expression(self) -> str:
        return self._filter.to_expression()

    @classmethod
    def equal(cls, field_name: str, value: DataValue) -> Condition:
        return cls(EqualFilter(field_name=field_name, value=value))

    @classmethod
    def not_equal(cls, field_name: str, value: DataValue) -> Condition:
        return cls(NotEqualFilter(field_name=field_name, value=value))

    @classmethod
    def less_than(cls, field_name: str, value: DataValue) -> Condition:
        return cls(LessThanFilter(field_name=field_name, value=value))

    @classmethod
    def less_than_or_equal(cls, field_name: str, value: DataValue) -> Condition:
        return cls(LessThanOrEqualFilter(field_name=field_name, value=value))

    @classmethod
    def greater_than(cls, field_name: str, value: DataValue) -> Condition:
        return cls(GreaterThanFilter(field_name=field_name, value=value))

    @classmethod
    def greater_than_or_equal(cls, field_name: str, value: DataValue) -> Condition:
        return cls(GreaterThanOrEqualFilter(field_name=field_name, value=value))

    @classmethod
    def is_in(cls, field_name: str, values: Sequence[DataValue]) -> Condition:
        return cls(InFilter(field_name=field_name, values=values))

    @classmethod
    def not_in(cls, field_name: str, values: Sequence[DataValue]) -> Condition:
        return cls(NotInFilter(field_name=field_name, values=values))

    @classmethod
    def between(cls, field_name: str, left: DataValue, right: DataValue) -> Condition:
        return cls(BetweenFilter(field_name=field_name, left=left, right=right))

    @classmethod
    def contains(cls, field_name: str, value: DataValue) -> Condition:
        return cls(ContainsFilter(field_name=field_name, value=value))

    @classmethod
    def not_contains(cls, field_name: str, value: DataValue) -> Condition:
        return cls(NotContainsFilter(field_name=field_name, value=value))

    @classmethod
    def starts_with(cls, field_name: str, value: DataValue) -> Condition:
        return cls(StartsWithFilter(field_name=field_name, value=value))

    @classmethod
    def ends_with(cls, field_name: str, value: DataValue) -> Condition:
        return cls(EndsWithFilter(field_name=field_name, value=value))

    @classmethod
    def is_null(cls, field_name: str) -> Condition:
        return cls(IsNullFilter(field_name=field_name))

    @classmethod
    def is_not_null(cls, field_name: str) -> Condition:
        return cls(IsNotNullFilter(field_name=field_name))


class PredicateGroup(Predicate):

    def __init__(self, operator: LogicalOperator, predicates: Sequence[Predicate] = None):
        self._operator = operator
        self._predicate = tuple(predicates) if predicates else tuple()

    @property
    def operator(self) -> LogicalOperator:
        return self._operator

    @property
    def predicates(self) -> tuple[Predicate, ...]:
        return self._predicate

    @property
    def is_leaf_node(self) -> bool:
        return len(self._predicate) == 1 and not isinstance(self._predicate[0], PredicateGroup)

    def to_expression(self) -> str:
        if not self.predicates:
            return ""

        expressions = []
        for predicate in self.predicates:
            expr = predicate.to_expression()
            if isinstance(predicate, PredicateGroup):
                expr = f"({expr})"
            expressions.append(expr)

        separator = f" {self.operator.value} "

        return separator.join(expressions)

    def __and__(self, other: PredicateGroup) -> PredicateGroup:
        if self.operator != other.operator:
            return PredicateGroup(self.operator, [self, other])
        return PredicateGroup(self.operator, [*self.predicates, *other.predicates])

    def __or__(self, other: PredicateGroup) -> PredicateGroup:
        if self.operator != other.operator:
            return PredicateGroup(self.operator, [self, other])
        return PredicateGroup(self.operator, [*self.predicates, *other.predicates])


class SortDirection(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class SortOrder:

    def __init__(self, field_name: str, direction: SortDirection = SortDirection.ASC):
        self._field_name = field_name
        self._direction = direction

    @property
    def field_name(self) -> str:
        return self._field_name

    @property
    def direction(self) -> SortDirection:
        return self._direction

    def to_expression(self) -> str:
        return f"{self.field_name} {self.direction.value}"


class Pagination:

    def __init__(self, limit: int = 50, offset: int = 0):
        if limit < 0 or offset < 0:
            ValueError(f"Pagination values are invalid. Limit and offset must be positive integers")

        self._limit = limit if limit < 100 else 100
        self._offset = offset

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def offset(self) -> int:
        return self._offset

    def to_expression(self) -> str:
        return f"LIMIT {self.limit} OFFSET {self.offset}"


class Specification(ABC):

    @abstractmethod
    def to_expression(self) -> str:
        pass


class QuerySpecification(Specification):

    def __init__(self, pagination: Pagination, sorting: Sequence[SortOrder] = None, predicate: Predicate = None):
        self._predicate = predicate
        self._sorting = tuple(sorting) if sorting else tuple()
        self._pagination = pagination

    @property
    def predicate(self) -> Predicate | None:
        return self._predicate

    @property
    def sorting(self) -> tuple[SortOrder, ...]:
        return self._sorting

    @property
    def pagination(self) -> Pagination:
        return self._pagination

    def to_expression(self) -> str:
        parts: list[str] = []

        if self.predicate:
            parts.append(f"WHERE {self.predicate.to_expression()}")

        if self.sorting:
            sorting_expression = ", ".join(sort.to_expression() for sort in self.sorting)
            parts.append(f"ORDER BY {sorting_expression}")

        parts.append(self.pagination.to_expression())

        return " ".join(parts)
