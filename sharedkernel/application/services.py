import contextvars
import typing
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from logging import Logger
from types import get_original_bases
from uuid import UUID

from sharedkernel.application.commands import Acknowledgement, Command, CommandHandler
from sharedkernel.application.errors import HandlerAlreadyRegistered, Rejection, ServiceBusErrors, UnsupportedHandler
from sharedkernel.application.queries import Query, QueryHandler
from sharedkernel.application.validators import ValidationResult, Validator
from sharedkernel.domain.data import ReadModel, ReadModelList
from sharedkernel.domain.errors import DomainException, EntityNotFound, UnhandledEventType

type Handler = CommandHandler[Command] | QueryHandler[Query]
type Request = Command | Query
type Response = Acknowledgement | ReadModel | ReadModelList


class ApplicationService:
    """Application Service marker class"""


class Sender(ABC):
    """Request Sender Interface"""

    @abstractmethod
    def register(self, handler: Handler | Validator[Command | Query]) -> bool:
        """Register a handler to process a request when a message is sent.

            Args:
                handler: Can be a Command Handler, a Query Handler or a Validator.
            """
        ...

    @abstractmethod
    def send(self, request: Request) -> Response | Rejection:
        """Routes a request to a particular handler.

            Args:
                request: Can be a Command or Query Handler.
            """
        ...


request_id_var: contextvars.ContextVar[UUID] = contextvars.ContextVar("request-id")


@dataclass(frozen=True)
class RequestContext:
    """Encapsulates the context of an incoming request."""
    request_id: UUID
    timestamp: datetime

    @staticmethod
    def new(request_id: UUID, timestamp: datetime | None = None) -> "RequestContext":
        """Creates a new request context.

        Args:
            request_id: A unique identifier for the request.
            timestamp: The timestamp of the request. If None, the current UTC time is used.
        """
        return RequestContext(
            request_id=request_id,
            timestamp=timestamp or datetime.now(UTC)
        )


def get_request_id() -> UUID:
    """Retrieves the current request ID from the context variable.

    Returns:
        The current request ID or a new UUID if not set.
    """
    return request_id_var.get(uuid.uuid4())


class ServiceBus:
    """Service Bus

    Communication mechanism used to decouple the sender of a message from its handler.
    Supports Commands, Queries, and Validators.
    Service Bus sends Request and returns Response.
    """

    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        self._command_handlers: dict[str, CommandHandler[Command]] = {}
        self._query_handlers: dict[str, QueryHandler[Query]] = {}
        self._validators: dict[str, Validator[Command | Query]] = {}

    def register(self, handler: Handler | Validator[Command | Query]) -> bool:
        """Registers a handler or validator to the service bus.

        Args:
            handler: The Command Handler, Query Handler, or Validator to register.

        Returns:
            True if registration was successful.

        Raises:
            HandlerAlreadyRegistered: If a handler is already registered for the request type.
            UnsupportedHandler: If the handler type is not supported.
        """
        bases = get_original_bases(handler.__class__)
        args = typing.get_args(bases[0])
        request_type = args[0].__name__

        if isinstance(handler, CommandHandler):
            if request_type in self._command_handlers:
                self._logger.error(f"A handler for {request_type} was already registered")
                raise HandlerAlreadyRegistered(self, request_type)
            self._logger.debug(f"{type(handler).__name__} was successfully registered")
            self._command_handlers[request_type] = handler
            return True

        if isinstance(handler, QueryHandler):
            if request_type in self._query_handlers:
                self._logger.error(f"A handler for {request_type} was already registered")
                raise HandlerAlreadyRegistered(self, request_type)
            self._logger.debug(f"{type(handler).__name__} was successfully registered")
            self._query_handlers[request_type] = handler
            return True

        if isinstance(handler, Validator):
            self._logger.debug(f"{type(handler).__name__} was successfully registered")
            self._validators[request_type] = handler
            return True

        self._logger.error(f"{type(self).__name__} cannot register {type(handler).__name__}")
        handler_type = type(handler).__name__
        raise UnsupportedHandler(self, handler_type)

    def send(self, request: Request, context: RequestContext) -> Response | Rejection:
        """Sends a request through the service bus.

        Sets the request ID in the context, processes the request, and performs post-processing.

        Args:
            request: The Command or Query to send.
            context: The request context.

        Returns:
            The response from the handler or a Rejection if an error occurs.
        """
        token = request_id_var.set(context.request_id)
        try:
            self._logger.info(f"{type(request).__name__} request received")
            process_result = self.process(request)
            response = self.post_process(process_result)
        except UnhandledEventType as error:
            self._logger.error(f"A {type(error).__name__} occurred when processing request {type(request).__name__}")
            response = Rejection.from_exception(status_code=500, error=error)
        except EntityNotFound as error:
            self._logger.error(f"A {type(error).__name__} occurred when processing request {type(request).__name__}")
            response = Rejection.from_exception(status_code=404, error=error)
        except DomainException as error:
            self._logger.error(f"A {type(error).__name__} occurred when processing request {type(request).__name__}")
            response = Rejection.from_exception(status_code=409, error=error)
        finally:
            request_id_var.reset(token)

        return response

    def process(self, request: Request) -> Response | Rejection:
        """Processes a request by validating it and routing it to the appropriate handler.

        Args:
            request: The request to process.

        Returns:
            The response from the handler or a Rejection if validation fails or no handler is found.
        """
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

    def pre_process(self, request: Request) -> ValidationResult:
        """Performs pre-processing validation on a request.

        Args:
            request: The request to validate.

        Returns:
            A ValidationResult indicating success or containing errors.
        """
        request_type = type(request).__name__

        if request_type not in self._validators:
            self._logger.debug(f"No validator registered for request {type(request).__name__}")
            return ValidationResult.success()

        validator = self._validators[request_type]

        return validator.validate(request)

    def process_command(self, command: Command) -> Acknowledgement | Rejection:
        """Directly processes a command using its registered handler.

        Args:
            command: The command to process.

        Returns:
            An Acknowledgement if successful, or a Rejection if no handler is registered.

        Raises:
            DomainException: If a business rule is violated during command execution.
        """
        command_type = type(command).__name__

        if command_type not in self._command_handlers:
            self._logger.warning(f"No handler registered for request {type(command).__name__}")
            error = ServiceBusErrors.no_handler_registered_for_request(command_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._command_handlers[command_type]

        return handler.execute(command)

    def process_query(self, query: Query) -> ReadModel | ReadModelList | Rejection:
        """Directly processes a query using its registered handler.

        Args:
            query: The query to process.

        Returns:
            The query result (ReadModel or ReadModelList) if successful, or a Rejection if no handler is registered.

        Raises:
            DomainException: If a business rule is violated during query execution.
        """
        query_type = type(query).__name__

        if query_type not in self._query_handlers:
            self._logger.warning(f"No handler registered for request {type(query).__name__}")
            error = ServiceBusErrors.no_handler_registered_for_request(query_type)
            return Rejection.from_error(status_code=501, error=error)

        handler = self._query_handlers[query_type]

        return handler.execute(query)

    def post_process(self, response: Response | Rejection) -> Response | Rejection:
        """Performs post-processing cleanup and logging after a request is handled.

        Args:
            response: The response from the handler.

        Returns:
            The original response.
        """
        if isinstance(response, Acknowledgement):
            self._logger.info(f"Request {response.action} {response.status}")

        if isinstance(response, ReadModel):
            self._logger.info(f"Request completed successfully returning a {type(response).__name__}")

        if isinstance(response, ReadModelList):
            items_type = type(response.items).__name__
            self._logger.info(f"Request completed successfully returning a {items_type} with {response.total} items")

        return response
