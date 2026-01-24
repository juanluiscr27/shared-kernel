from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import List, Any

from sharedkernel.application.validators import ValidationResult
from sharedkernel.domain.errors import Error, DomainError, ServiceError

ERROR_CONTEXT = 'error'


class ApplicationError(ServiceError):
    """Application Error

    Represents an error that occurred during the orchestration of the business logic.

    Args:
        service: Service on which the error was raised.
        message: Human readable string describing the exception.
    """

    def __init__(self, service: object, message: str):
        super().__init__(message)
        service_module = service.__module__
        service_name = service.__name__
        self.service = f"{service_module}.{service_name}"


class HandlerAlreadyRegistered(ApplicationError):

    def __init__(self, service: object, request_type: str):
        message = f"A Handler has been already registered for `{request_type}`"
        super().__init__(type(service), message)


class UnsupportedHandler(ApplicationError):

    def __init__(self, service: object, handler: str):
        service_name = type(service).__name__
        message = f"`{handler}` cannot be registered to {service_name}"
        super().__init__(type(service), message)


class ServiceBusErrors:
    """
    Catalog of Errors for a Service Bus.
    """

    @staticmethod
    def request_not_supported(request_type: str) -> Error:
        return Error(
            message=f"Request '{request_type} cannot be handled by the Service Bus'.",
            code="ServiceBus.Request.NotSupported",
            reason="Service Bus only supports requests of type Command or Query.",
            domain="SharedKernel.Application.ServiceBus",
        )

    @staticmethod
    def no_handler_registered_for_request(request_type: str) -> Error:
        return Error(
            message=f"Request '{request_type} has not handler registered the Service Bus'.",
            code="ServiceBus.Request.NoHandlerRegistered",
            reason="No handler was found in the Service Bus for this request.",
            domain="SharedKernel.Application.ServiceBus",
        )


class ErrorDetail(SimpleNamespace):
    """Error Detail

    A standard machine-readable details of errors in an HTTP response.

    Attributes:
        loc: A reference that identifies the specific instance where the error occurred.
        msg: A short summary to describe the type of error in general.
        type: Identifies the error type.
    """
    loc: List[str]
    msg: str
    type: str

    def asdict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass(frozen=True)
class Rejection:
    """Request Rejection

    Represents a rejection of a command or a query. Commonly used when a validation fails or
    a business rule is broken.

    Attributes:
        status_code: Numeric value that indicates the status of the response.
        errors: A list of error details.
    """

    status_code: int
    errors: List[ErrorDetail] = field(default_factory=list)

    @classmethod
    def default(cls):
        error = ErrorDetail(
            loc=["Application.Service", ],
            msg="Unknown error occurred.",
            type="ServiceBus.Request.ProcessRequest",
        )
        error.ctx = {ERROR_CONTEXT: "Unknown error"}

        return cls(status_code=501, errors=[error, ])

    @classmethod
    def from_validation(cls, result: ValidationResult):
        errors = []
        for result_error in result.errors:
            error = ErrorDetail(
                loc=[result_error.domain, ],
                msg=result_error.message,
                type=result_error.code,
            )
            error.ctx = {ERROR_CONTEXT: result_error.reason}

            errors.append(error)

        return cls(status_code=400, errors=errors)

    @classmethod
    def from_error(cls, status_code: int, error: Error):
        error_detail = ErrorDetail(
            loc=[error.domain, ],
            msg=error.message,
            type=error.code,
        )

        error_detail.ctx = {ERROR_CONTEXT: error.reason}

        return cls(status_code=status_code, errors=[error_detail])

    @classmethod
    def from_exception(cls, status_code: int, error: DomainError):
        module = type(error).__module__
        error_name = type(error).__name__
        error_type = f"{module}.{error_name}"

        error_detail = ErrorDetail(
            loc=[error.domain, ],
            msg=error.message,
            type=error_type,
        )

        return cls(status_code=status_code, errors=[error_detail])
