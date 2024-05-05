from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ReadModel:
    """ReadModel base class

    Is a Data Transfer Object used to provide cohesive information about an entity to queries.
    """


@dataclass(frozen=True)
class ReadModelList:
    """ReadModelList class

    Is an object that represents a group of `ReadModel` entities structured as a limit-offset based pagination.

    Args:
        offset: number of skipped items.
        limit: number of items per page.
        total: total number of items.
        items: list of `ReadModel` paginated items.
    """
    offset: int
    limit: int
    total: int
    items: List[ReadModel]
