from collections import deque
from typing import get_args, Generic, TypeVar, Deque, Any
from abc import abstractmethod, ABC
from types import get_original_bases
from typing import Optional, Self

from sharedkernel.api.contracts import Request
from sharedkernel.api.errors import RequestMapperNotFound
from sharedkernel.application.commands import Command
from sharedkernel.application.queries import Query

TRequest = TypeVar("TRequest", bound=Request)
TMessage = TypeVar("TMessage", bound=Command | Query)


class RequestMapper(ABC, Generic[TRequest]):
    """Base class for request mappers that convert API requests into application messages."""

    def __init__(self):
        self._next: Optional[Self] = None

    @property
    def request_type(self) -> str:
        """Returns the name of the request type this mapper handles."""
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    def set_next(self, mapper: Self) -> None:
        """Sets the next mapper in the chain.

        Args:
            mapper: The next RequestMapper instance.
        """
        self._next = mapper

    @abstractmethod
    def map(self, request: TRequest, **query_params: Any) -> Optional[TMessage]:
        """Maps an API request to an application Command or Query.

        Args:
            request: The API request object.
            **query_params: Additional parameters from the request query string.

        Returns:
            The mapped application message or None if not handled.
        """
        ...

    def map_next(self, request: TRequest, **query_params: Any) -> Optional[TMessage]:
        """Delegates mapping to the next mapper in the chain.

        Args:
            request: The API request object.
            **query_params: Additional parameters.

        Returns:
            The result of the next mapper, or None if no next mapper exists.
        """
        if not self._next:
            return None

        return self._next.map(request, **query_params)


class RequestMappingBehavior(ABC):
    """Abstract base class defining the behavior for mapping requests."""

    @abstractmethod
    def map(self, request: TRequest, **query_params: Any) -> TMessage:
        """Maps an API request to an application message.

        Args:
            request: The API request object.
            **query_params: Additional parameters.

        Returns:
            The mapped application message.
        """
        ...


class RequestMappersChain(RequestMappingBehavior):
    """A chain of request mappers that attempts to map a request using each mapper in sequence."""

    def __init__(self):
        self._mappers: Deque[RequestMapper] = deque()
        self._first: Optional[RequestMapper] = None

    def __call__(self, request: TRequest, **query_params: Any) -> TMessage:
        """Makes the chain callable, delegating to the map method."""
        return self.map(request, **query_params)

    def add(self, mapper: RequestMapper) -> None:
        """Adds a mapper to the beginning of the chain.

        Args:
            mapper: The RequestMapper instance to add.
        """
        if self._first:
            mapper.set_next(self._first)

        self._mappers.appendleft(mapper)
        self._first = mapper

    def map(self, request: TRequest, **query_params: Any) -> TMessage:
        """Attempts to map the request by passing it through the chain.

        Args:
            request: The API request object.
            **query_params: Additional parameters.

        Returns:
            The first successfully mapped message from the chain.

        Raises:
            RequestMapperNotFound: If the chain is empty or no mapper could handle the request.
        """
        if not self._first:
            raise RequestMapperNotFound(self, type(request).__name__)

        message = self._first.map(request, **query_params)
        if not message:
            raise RequestMapperNotFound(self, type(request).__name__)

        return message
