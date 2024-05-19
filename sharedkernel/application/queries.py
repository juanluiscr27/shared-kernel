from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from result import Result

from sharedkernel.domain.data import ReadModel, ReadModelList
from sharedkernel.domain.errors import Error


@dataclass(frozen=True)
class Query:
    """Query base class

    A Query is an object that encapsulates a request into a single entity that contains all information about
    the request.
    """


TQuery = TypeVar("TQuery", bound=Query)
TResult = TypeVar("TResult", bound=ReadModel | ReadModelList)


class QueryHandler(ABC, Generic[TQuery]):
    """Query Handler

    Is an object that defines a method to execute data retrieval.
    Query Handlers take a `Query` as input,
    search on the data store based on the query parameters and return a `ReadModel` or `ReadModelList`.
    """

    @abstractmethod
    def execute(self, query: TQuery) -> Result[TResult, Error]:
        """Execute a Query.

        Args:
            query: Query to execute.

        Returns:
            The execution result of the query.
            It could be a `ReadModel`, a `ReadModelList` or an `Error`.
        """
