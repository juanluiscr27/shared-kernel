from collections import deque
from typing import get_args, Generic, TypeVar, Deque
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

    def __init__(self):
        self._next: Optional[Self] = None

    @property
    def request_type(self) -> str:
        bases = get_original_bases(self.__class__)
        args = get_args(bases[0])
        return args[0].__name__

    def set_next(self, mapper: Self):
        self._next = mapper

    @abstractmethod
    def map(self, request: TRequest, **query_params) -> Optional[TMessage]:
        ...

    def map_next(self, request: TRequest, **query_params) -> Optional[TMessage]:
        if not self._next:
            return None

        return self._next.map(request, **query_params)


class RequestMappingBehavior(ABC):
    def map(self, request: TRequest, **query_params) -> TMessage:
        ...


class RequestMappersChain(RequestMappingBehavior):

    def __init__(self):
        self._mappers: Deque[RequestMapper] = deque()
        self._first: Optional[RequestMapper] = None

    def add(self, mapper: RequestMapper) -> None:
        if self._first:
            mapper.set_next(self._first)

        self._mappers.appendleft(mapper)
        self._first = mapper

    def map(self, request: TRequest, **query_params) -> TMessage:
        if not self._first:
            raise RequestMapperNotFound(self, request)

        message = self._first.map(request, **query_params)
        if not message:
            raise RequestMapperNotFound(self, request)

        return message
