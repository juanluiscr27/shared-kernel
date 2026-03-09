from abc import ABC, abstractmethod
from dataclasses import dataclass

from sharedkernel.domain.data import ReadModel, ReadModelList


@dataclass(frozen=True)
class Query:
    """Query base class

    A Query is an object that encapsulates a request into a single entity that contains all information about
    the request.
    """


class QueryHandler[TQuery: Query](ABC):
    """Query Handler

    Is an object that defines a method to execute data retrieval.
    Query Handlers take a `Query` as input,
    search on the data store based on the query parameters and return a `ReadModel` or `ReadModelList`.
    """

    @abstractmethod
    def execute(self, query: TQuery) -> ReadModel | ReadModelList:
        """Execute a Query.

        Args:
            query: Query to execute.

        Returns:
            A `ReadModel` or `ReadModelList` with the query results.

        Raises:
            DomainException: If a business rule is violated.
        """
