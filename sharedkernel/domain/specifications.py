"""Query Specification pattern for building composable query predicates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum
from itertools import count
from typing import LiteralString
from uuid import UUID


class LogicalOperator(StrEnum):
    """Logical operators for combining predicates."""

    AND = "AND"
    OR = "OR"


class Predicate(ABC):
    """Abstract base for query predicates."""

    @abstractmethod
    def to_expression(self) -> str:
        """Returns the predicate as a SQL expression string."""

    def build_template(self, _counter: count[int], _alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        return "", {}


class Filter(Predicate):
    """Base class for field-level filter predicates."""

    def __init__(self, field_name: str) -> None:
        self._field_name: LiteralString = field_name

    @property
    def field_name(self) -> LiteralString:
        """The name of the field this filter applies to."""
        return self._field_name

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return ""


DataValue = str | int | float | bool | datetime | UUID


def format_value(value: DataValue) -> str:
    """Formats a data value for use in a SQL expression."""
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
    """Formats a sequence of data values as a parenthesized, comma-separated list."""
    formatted = ", ".join(format_value(value) for value in values)

    return f"({formatted})"


def _escape_like(value: DataValue) -> str:
    """Escapes LIKE-special characters in a value for safe use in LIKE patterns."""
    return str(value).replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _clean_alias(alias: str) -> str:
    """Strips whitespace and removes dots from a table alias."""
    return alias.strip().replace(".", "")


def _qualify(field_name: LiteralString, alias: str) -> str:
    """Prepends a table alias to a field name when the alias is non-empty."""
    if alias:
        return f"{alias}.{field_name}"
    return field_name


class EqualFilter(Filter):
    """Filter for equality comparison (field = value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} = {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} = %({key})s", {key: self._raw_value}


class NotEqualFilter(Filter):
    """Filter for inequality comparison (field != value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} != {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} != %({key})s", {key: self._raw_value}


class LessThanFilter(Filter):
    """Filter for less-than comparison (field < value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} < {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} < %({key})s", {key: self._raw_value}


class LessThanOrEqualFilter(Filter):
    """Filter for less-than-or-equal comparison (field <= value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} <= {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} <= %({key})s", {key: self._raw_value}


class GreaterThanFilter(Filter):
    """Filter for greater-than comparison (field > value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} > {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} > %({key})s", {key: self._raw_value}


class GreaterThanOrEqualFilter(Filter):
    """Filter for greater-than-or-equal comparison (field >= value)."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = format_value(value)
        self._raw_value = value

    @property
    def value(self) -> str:
        """The formatted value to compare against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} >= {self.value}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        key = f"p{next(counter)}"
        field = _qualify(self.field_name, alias)
        return f"{field} >= %({key})s", {key: self._raw_value}


class InFilter(Filter):
    """Filter for set membership (field IN (values))."""

    def __init__(self, field_name: str, values: Sequence[DataValue]) -> None:
        super().__init__(field_name)
        self._values = format_iterable(values)
        self._raw_values = tuple(values)

    @property
    def values(self) -> str:
        """The formatted list of values."""
        return self._values

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} IN {self.values}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        params: dict[str, DataValue] = {}
        placeholders: list[str] = []
        for val in self._raw_values:
            key = f"p{next(counter)}"
            params[key] = val
            placeholders.append(f"%({key})s")
        joined = ", ".join(placeholders)
        return f"{field} IN ({joined})", params


class NotInFilter(Filter):
    """Filter for set exclusion (field NOT IN (values))."""

    def __init__(self, field_name: str, values: Sequence[DataValue]) -> None:
        super().__init__(field_name)
        self._values = format_iterable(values)
        self._raw_values = tuple(values)

    @property
    def values(self) -> str:
        """The formatted list of values."""
        return self._values

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} NOT IN {self.values}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        params: dict[str, DataValue] = {}
        placeholders: list[str] = []
        for val in self._raw_values:
            key = f"p{next(counter)}"
            params[key] = val
            placeholders.append(f"%({key})s")
        joined = ", ".join(placeholders)
        return f"{field} NOT IN ({joined})", params


class BetweenFilter(Filter):
    """Filter for range inclusion (field BETWEEN left AND right)."""

    def __init__(self, field_name: str, left: DataValue, right: DataValue) -> None:
        super().__init__(field_name)
        self._left_value = format_value(left)
        self._right_value = format_value(right)
        self._raw_left = left
        self._raw_right = right

    @property
    def left(self) -> str:
        """The formatted lower bound."""
        return self._left_value

    @property
    def right(self) -> str:
        """The formatted upper bound."""
        return self._right_value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} BETWEEN {self.left} AND {self.right}"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        k1 = f"p{next(counter)}"
        k2 = f"p{next(counter)}"
        return f"{field} BETWEEN %({k1})s AND %({k2})s", {k1: self._raw_left, k2: self._raw_right}


class ContainsFilter(Filter):
    """Filter for substring match (field LIKE '%value%')."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = value

    @property
    def value(self) -> DataValue:
        """The value to match against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} LIKE '%{self.value}%'"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        key = f"p{next(counter)}"
        escaped = _escape_like(self.value)
        return f"{field} LIKE %({key})s", {key: f"%{escaped}%"}


class NotContainsFilter(Filter):
    """Filter for substring exclusion (field NOT LIKE '%value%')."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = value

    @property
    def value(self) -> DataValue:
        """The value to match against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} NOT LIKE '%{self.value}%'"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        key = f"p{next(counter)}"
        escaped = _escape_like(self.value)
        return f"{field} NOT LIKE %({key})s", {key: f"%{escaped}%"}


class StartsWithFilter(Filter):
    """Filter for prefix match (field LIKE 'value%')."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = value

    @property
    def value(self) -> DataValue:
        """The value to match against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} LIKE '{self.value}%'"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        key = f"p{next(counter)}"
        escaped = _escape_like(self.value)
        return f"{field} LIKE %({key})s", {key: f"{escaped}%"}


class EndsWithFilter(Filter):
    """Filter for suffix match (field LIKE '%value')."""

    def __init__(self, field_name: str, value: DataValue) -> None:
        super().__init__(field_name)
        self._value = value

    @property
    def value(self) -> DataValue:
        """The value to match against."""
        return self._value

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} LIKE '%{self.value}'"

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        key = f"p{next(counter)}"
        escaped = _escape_like(self.value)
        return f"{field} LIKE %({key})s", {key: f"%{escaped}"}


class IsNullFilter(Filter):
    """Filter for null check (field IS NULL)."""

    def __init__(self, field_name: str) -> None:
        super().__init__(field_name)

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} IS NULL"

    def build_template(self, _counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        return f"{field} IS NULL", {}


class IsNotNullFilter(Filter):
    """Filter for non-null check (field IS NOT NULL)."""

    def __init__(self, field_name: str) -> None:
        super().__init__(field_name)

    def to_expression(self) -> str:
        """Returns the filter as a SQL expression string."""
        return f"{self.field_name} IS NOT NULL"

    def build_template(self, _counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        field = _qualify(self.field_name, alias)
        return f"{field} IS NOT NULL", {}


class Condition(Predicate):
    """A predicate that wraps a Filter with factory classmethods for creation."""

    def __init__(self, predicate_filter: Filter) -> None:
        self._filter = predicate_filter

    def to_expression(self) -> str:
        """Returns the condition as a SQL expression string."""
        return self._filter.to_expression()

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        return self._filter.build_template(counter, alias)

    @classmethod
    def equal(cls, field_name: str, value: DataValue) -> Condition:
        """Creates an equality condition (field = value)."""
        return cls(EqualFilter(field_name=field_name, value=value))

    @classmethod
    def not_equal(cls, field_name: str, value: DataValue) -> Condition:
        """Creates an inequality condition (field != value)."""
        return cls(NotEqualFilter(field_name=field_name, value=value))

    @classmethod
    def less_than(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a less-than condition (field < value)."""
        return cls(LessThanFilter(field_name=field_name, value=value))

    @classmethod
    def less_than_or_equal(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a less-than-or-equal condition (field <= value)."""
        return cls(LessThanOrEqualFilter(field_name=field_name, value=value))

    @classmethod
    def greater_than(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a greater-than condition (field > value)."""
        return cls(GreaterThanFilter(field_name=field_name, value=value))

    @classmethod
    def greater_than_or_equal(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a greater-than-or-equal condition (field >= value)."""
        return cls(GreaterThanOrEqualFilter(field_name=field_name, value=value))

    @classmethod
    def is_in(cls, field_name: str, values: Sequence[DataValue]) -> Condition:
        """Creates a set membership condition (field IN (values))."""
        return cls(InFilter(field_name=field_name, values=values))

    @classmethod
    def not_in(cls, field_name: str, values: Sequence[DataValue]) -> Condition:
        """Creates a set exclusion condition (field NOT IN (values))."""
        return cls(NotInFilter(field_name=field_name, values=values))

    @classmethod
    def between(cls, field_name: str, left: DataValue, right: DataValue) -> Condition:
        """Creates a range condition (field BETWEEN left AND right)."""
        return cls(BetweenFilter(field_name=field_name, left=left, right=right))

    @classmethod
    def contains(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a substring match condition (field LIKE '%value%')."""
        return cls(ContainsFilter(field_name=field_name, value=value))

    @classmethod
    def not_contains(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a substring exclusion condition (field NOT LIKE '%value%')."""
        return cls(NotContainsFilter(field_name=field_name, value=value))

    @classmethod
    def starts_with(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a prefix match condition (field LIKE 'value%')."""
        return cls(StartsWithFilter(field_name=field_name, value=value))

    @classmethod
    def ends_with(cls, field_name: str, value: DataValue) -> Condition:
        """Creates a suffix match condition (field LIKE '%value')."""
        return cls(EndsWithFilter(field_name=field_name, value=value))

    @classmethod
    def is_null(cls, field_name: str) -> Condition:
        """Creates a null check condition (field IS NULL)."""
        return cls(IsNullFilter(field_name=field_name))

    @classmethod
    def is_not_null(cls, field_name: str) -> Condition:
        """Creates a non-null check condition (field IS NOT NULL)."""
        return cls(IsNotNullFilter(field_name=field_name))


class PredicateGroup(Predicate):
    """A composite predicate that combines predicates with a logical operator."""

    def __init__(self, operator: LogicalOperator, predicates: Sequence[Predicate] | None = None) -> None:
        self._operator = operator
        self._predicate = tuple(predicates) if predicates else ()

    @property
    def operator(self) -> LogicalOperator:
        """The logical operator used to combine predicates."""
        return self._operator

    @property
    def predicates(self) -> tuple[Predicate, ...]:
        """The predicates in this group."""
        return self._predicate

    def to_expression(self) -> str:
        """Returns the predicate group as a SQL expression string."""
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

    def build_template(self, counter: count[int], alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Builds a parameterized SQL template fragment using the shared parameter counter."""
        if not self.predicates:
            return "", {}

        templates: list[str] = []
        all_params: dict[str, DataValue] = {}
        for predicate in self.predicates:
            tmpl, params = predicate.build_template(counter, alias)
            if isinstance(predicate, PredicateGroup):
                tmpl = f"({tmpl})"
            templates.append(tmpl)
            all_params.update(params)

        separator = f" {self.operator.value} "
        return separator.join(templates), all_params

    def __and__(self, other: PredicateGroup) -> PredicateGroup:
        if self.operator != other.operator:
            return PredicateGroup(self.operator, [self, other])
        return PredicateGroup(self.operator, [*self.predicates, *other.predicates])

    def __or__(self, other: PredicateGroup) -> PredicateGroup:
        if self.operator != other.operator:
            return PredicateGroup(self.operator, [self, other])
        return PredicateGroup(self.operator, [*self.predicates, *other.predicates])


class SortDirection(StrEnum):
    """Sort direction for ordering query results."""

    ASC = "ASC"
    DESC = "DESC"


class SortOrder:
    """Defines a sort order for a field in a query."""

    def __init__(self, field_name: str, direction: SortDirection = SortDirection.ASC) -> None:
        self._field_name = field_name
        self._direction = direction

    @property
    def field_name(self) -> str:
        """The name of the field to sort by."""
        return self._field_name

    @property
    def direction(self) -> SortDirection:
        """The sort direction."""
        return self._direction

    def to_expression(self) -> str:
        """Returns the sort order as a SQL expression string."""
        return f"{self.field_name} {self.direction.value}"


class Pagination:
    """Defines pagination parameters for a query."""

    MAX_LIMIT = 100

    def __init__(self, limit: int = 50, offset: int = 0) -> None:
        if limit < 0 or offset < 0:
            raise ValueError("Pagination values are invalid. Limit and offset must be positive integers")

        self._limit = limit if limit < self.MAX_LIMIT else self.MAX_LIMIT
        self._offset = offset

    @property
    def limit(self) -> int:
        """The maximum number of results to return."""
        return self._limit

    @property
    def offset(self) -> int:
        """The number of results to skip."""
        return self._offset

    def to_expression(self) -> str:
        """Returns the pagination as a SQL expression string."""
        return f"LIMIT {self.limit} OFFSET {self.offset}"


class Specification(ABC):
    """Abstract base for query specifications."""

    @abstractmethod
    def to_expression(self) -> str:
        """Returns the specification as a SQL expression string."""

    @property
    @abstractmethod
    def limit(self) -> int:
        """The maximum number of results to return."""

    @property
    @abstractmethod
    def offset(self) -> int:
        """The number of results to skip."""


class QuerySpecification(Specification):
    """A complete query specification combining predicates, sorting, and pagination."""

    def __init__(
            self, pagination: Pagination,
            sorting: Sequence[SortOrder] | None = None,
            predicate: Predicate | None = None,
    ) -> None:
        self._predicate = predicate
        self._sorting = tuple(sorting) if sorting else ()
        self._pagination = pagination

    @property
    def predicate(self) -> Predicate | None:
        """The filter predicate for the query."""
        return self._predicate

    @property
    def sorting(self) -> tuple[SortOrder, ...]:
        """The sort orders for the query."""
        return self._sorting

    @property
    def pagination(self) -> Pagination:
        """The pagination parameters for the query."""
        return self._pagination

    @property
    def limit(self) -> int:
        """The maximum number of results to return."""
        return self._pagination.limit

    @property
    def offset(self) -> int:
        """The number of results to skip."""
        return self._pagination.offset

    def to_expression(self) -> str:
        """Returns the full query specification as a SQL expression string."""
        parts: list[str] = []

        if self.predicate:
            expr = self.predicate.to_expression()
            if expr:
                parts.append(f"WHERE {expr}")

        if self.sorting:
            sorting_expression = ", ".join(sort.to_expression() for sort in self.sorting)
            parts.append(f"ORDER BY {sorting_expression}")

        parts.append(self.pagination.to_expression())

        return " ".join(parts)

    def to_statement(self, alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Returns the full query specification as a parameterized SQL statement."""
        alias = _clean_alias(alias)
        parts: list[str] = []
        params: dict[str, DataValue] = {}
        counter = count()

        if self.predicate:
            tmpl, params = self.predicate.build_template(counter, alias)
            if tmpl:
                parts.append(f"WHERE {tmpl}")

        if self.sorting:
            sorting_expression = ", ".join(
                f"{_qualify(sort.field_name, alias)} {sort.direction.value}" for sort in self.sorting
            )
            parts.append(f"ORDER BY {sorting_expression}")

        parts.append(self.pagination.to_expression())

        return " ".join(parts), params

    def to_filter(self, alias: str = "") -> tuple[LiteralString, dict[str, DataValue]]:
        """Returns the filter predicate as a parameterized SQL WHERE clause."""
        if not self.predicate:
            return "", {}

        alias = _clean_alias(alias)
        counter = count()
        tmpl, params = self.predicate.build_template(counter, alias)
        if not tmpl:
            return "", {}
        return f"WHERE {tmpl}", params
