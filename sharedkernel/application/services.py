import typing
from abc import ABC, abstractmethod
from types import get_original_bases
from typing import Dict, TypeVar, Union

from result import Ok, Err

from sharedkernel.application.commands import Command, CommandHandler, Acknowledgement
from sharedkernel.application.errors import HandlerAlreadyRegistered, Rejection, UnsupportedHandler, ServiceBusErrors
from sharedkernel.application.queries import Query, QueryHandler, TResult
from sharedkernel.application.validators import Validator, ValidationResult, TRequest
from sharedkernel.domain.data import ReadModel, ReadModelList
from sharedkernel.domain.errors import DomainError


class ApplicationService:
    """Application Service marker class"""


THandler = TypeVar("THandler", bound=CommandHandler | QueryHandler)
TResponse = TypeVar("TResponse", bound=Acknowledgement | ReadModel | ReadModelList)


class Sender(ABC):
    """Request Sender Interface"""

    @abstractmethod
    def register(self, handler: Union[THandler, Validator]) -> bool:
        """Register a handler to process a request when a message is sent.

            Args:
                handler: Can be a Command Handler, a Query Handler or a Validator.
            """
        ...

    @abstractmethod
    def send(self, request: TRequest) -> Union[TResponse, Rejection]:
        """Routes a request to a particular handler.

            Args:
                request: Can be a Command or Query Handler.
            """
        ...


NOT_FOUND = 'NotFound'


class ServiceBus:
    """Service Bus

    Communication mechanism used to decouple the sender of a message from its handler.
    Supports Commands, Queries, and Validators.
    Service Bus sends Request and returns Response.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, THandler] = {}
        self._validators: Dict[str, Validator] = {}

    def register(self, handler: Union[THandler, Validator]) -> bool:
        bases = get_original_bases(handler.__class__)
        args = typing.get_args(bases[0])
        request_type = args[0].__name__

        if request_type in self._handlers:
            raise HandlerAlreadyRegistered(self, request_type)

        if isinstance(handler, CommandHandler | QueryHandler):
            self._handlers[request_type] = handler
            return True

        if isinstance(handler, Validator):
            self._validators[request_type] = handler
            return True

        handler_type = type(handler).__name__
        raise UnsupportedHandler(self, handler_type)

    def send(self, request: TRequest) -> Union[TResponse, Rejection]:
        try:
            return self.process(request)
        except DomainError as error:
            return Rejection.from_exception(status_code=422, error=error)

    def process(self, request: TRequest) -> TResponse:
        validation_result = self.pre_process(request)

        if not validation_result.is_valid:
            return Rejection.from_validation(validation_result)

        if isinstance(request, Command):
            return self.process_command(request)

        if isinstance(request, Query):
            return self.process_query(request)

        request_type = type(request).__name__
        error = ServiceBusErrors.request_not_supported(request_type)

        return Rejection.from_error(status_code=501, error=error)

    def pre_process(self, request: TRequest) -> ValidationResult:
        request_type = type(request).__name__

        if request_type not in self._validators:
            return ValidationResult.success()

        validators = self._validators[request_type]

        return validators.validate(request)

    def process_command(self, command: Command) -> Union[Acknowledgement, Rejection]:
        command_type = type(command).__name__

        if command_type not in self._handlers:
            error = ServiceBusErrors.no_handler_registered_for_request(command_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._handlers[command_type]

        result = handler.execute(command)

        match result:
            case Ok(ack):
                return ack
            case Err(error):
                status_code = 404 if NOT_FOUND in error.code else 422
                return Rejection.from_error(status_code=status_code, error=error)

    def process_query(self, query: Query) -> Union[TResult, Rejection]:
        query_type = type(query).__name__

        if query_type not in self._handlers:
            error = ServiceBusErrors.no_handler_registered_for_request(query_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._handlers[query_type]

        result = handler.execute(query)

        match result:
            case Ok(read_model):
                return read_model
            case Err(error):
                status_code = 404 if NOT_FOUND in error.code else 422
                return Rejection.from_error(status_code=status_code, error=error)
