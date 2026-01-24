import contextvars
import typing
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, UTC
from logging import Logger
from types import get_original_bases
from typing import Dict, TypeVar, Union, Optional
from uuid import UUID

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

request_id_var: contextvars.ContextVar[UUID] = contextvars.ContextVar("request-id")


@dataclass(frozen=True)
class RequestContext:
    request_id: UUID
    timestamp: datetime

    @staticmethod
    def new(request_id: UUID, timestamp: Optional[datetime]) -> "RequestContext":
        return RequestContext(
            request_id=request_id,
            timestamp=timestamp or datetime.now(UTC)
        )


def get_request_id() -> UUID:
    return request_id_var.get(uuid.uuid4())


class ServiceBus:
    """Service Bus

    Communication mechanism used to decouple the sender of a message from its handler.
    Supports Commands, Queries, and Validators.
    Service Bus sends Request and returns Response.
    """

    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        self._handlers: Dict[str, THandler] = dict()
        self._validators: Dict[str, Validator] = dict()

    def register(self, handler: Union[THandler, Validator]) -> bool:
        bases = get_original_bases(handler.__class__)
        args = typing.get_args(bases[0])
        request_type = args[0].__name__

        if request_type in self._handlers:
            self._logger.error(f"A handler for {request_type} was already registered")
            raise HandlerAlreadyRegistered(self, request_type)

        if isinstance(handler, CommandHandler | QueryHandler):
            self._logger.debug(f"{type(handler).__name__} was successfully registered")
            self._handlers[request_type] = handler
            return True

        if isinstance(handler, Validator):
            self._logger.debug(f"{type(handler).__name__} was successfully registered")
            self._validators[request_type] = handler
            return True

        self._logger.error(f"{type(self).__name__} cannot register {type(handler).__name__}")
        handler_type = type(handler).__name__
        raise UnsupportedHandler(self, handler_type)

    def send(self, request: TRequest, context: RequestContext) -> Union[TResponse, Rejection]:
        response = Rejection.default()
        token = request_id_var.set(context.request_id)
        try:
            self._logger.info(f"{type(request).__name__} request received")
            process_result = self.process(request)
            response = self.post_process(process_result)
        except DomainError as error:
            self._logger.error(f"A {type(error).__name__} occurred when processing request {type(request).__name__}")
            response = Rejection.from_exception(status_code=422, error=error)
        finally:
            request_id_var.reset(token)
            return response

    def process(self, request: TRequest) -> TResponse:
        validation_result = self.pre_process(request)

        if not validation_result.is_valid:
            self._logger.warning(f"Validation errors found in {type(request).__name__}")
            return Rejection.from_validation(validation_result)

        if isinstance(request, Command):
            return self.process_command(request)

        if isinstance(request, Query):
            return self.process_query(request)

        request_type = type(request).__name__
        error = ServiceBusErrors.request_not_supported(request_type)
        self._logger.warning(f"{type(self).__name__} cannot process {type(request).__name__} requests")
        return Rejection.from_error(status_code=501, error=error)

    def pre_process(self, request: TRequest) -> ValidationResult:
        request_type = type(request).__name__

        if request_type not in self._validators:
            self._logger.debug(f"No validator registered for request {type(request).__name__}")
            return ValidationResult.success()

        validator = self._validators[request_type]

        return validator.validate(request)

    def process_command(self, command: Command) -> Union[Acknowledgement, Rejection]:
        command_type = type(command).__name__

        if command_type not in self._handlers:
            self._logger.warning(f"No handler registered for request {type(command).__name__}")
            error = ServiceBusErrors.no_handler_registered_for_request(command_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._handlers[command_type]

        result = handler.execute(command)

        match result:
            case Ok(ack):
                return ack
            case Err(error):
                self._logger.error(error.message)
                status_code = 404 if NOT_FOUND in error.code else 422
                return Rejection.from_error(status_code=status_code, error=error)

    def process_query(self, query: Query) -> Union[TResult, Rejection]:
        query_type = type(query).__name__

        if query_type not in self._handlers:
            self._logger.warning(f"No handler registered for request {type(query).__name__}")
            error = ServiceBusErrors.no_handler_registered_for_request(query_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._handlers[query_type]

        result = handler.execute(query)

        match result:
            case Ok(read_model):
                return read_model
            case Err(error):
                self._logger.error(error.message)
                status_code = 404 if NOT_FOUND in error.code else 422
                return Rejection.from_error(status_code=status_code, error=error)

    def post_process(self, response: TResponse) -> TResponse:
        if isinstance(response, Acknowledgement):
            self._logger.info(f"Request {response.action} {response.status}")

        if isinstance(response, ReadModel):
            self._logger.info(f"Request completed successfully returning a {type(response).__name__}")

        if isinstance(response, ReadModelList):
            items_type = type(response.items).__name__
            self._logger.info(f"Request completed successfully returning a {items_type} with {response.total} items")

        return response
