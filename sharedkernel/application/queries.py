from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from sharedkernel.domain.models import ReadModel, ReadModelList


@dataclass(frozen=True)
class Query:
    """Query base class

    A Query is an object that encapsulates a request into a single entity that contains all information about
    the request.
    """


TResult = TypeVar("TResult", bound=ReadModel | ReadModelList)


class QueryHandler(ABC):
    """Query Handler

    Is an object that define methods executes data retrieval. Query Handlers take a `Query` as input, search on the data
    store based on the query parameters and return a `ReadModel` or `ReadModelList`.
    """

    @abstractmethod
    def execute(self, query: Query) -> TResult:
        """Execute a Command.

        Args:
            query (Query): Query to execute.

        Returns:
            TResult
        """
