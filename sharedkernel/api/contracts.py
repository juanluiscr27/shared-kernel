from typing import List

from pydantic import BaseModel

from sharedkernel.domain.errors import Error, DomainError


class Request(BaseModel):
    """Request base class

    Serves as a formal agreement to interact with the API resources.
    """


class Response(BaseModel):
    """Response base class

    An API contract that defines as a standard HTTP response structure.
    """


class ProblemDetail(Response):
    """ProblemDetail

    A standard machine-readable details of errors in an HTTP response.

    Args:
        loc: A reference that identifies the specific instance where the problem occurred.
        msg: A short summary to describe the type of problem in general.
        type: Identifies the problem type.
    """
    loc: List[str]
    msg: str
    type: str


class ErrorResponse(ProblemDetail):
    """ErrorResponse

        HTTP ProblemDetail response for application `Error`.

        Args:
            error: Application error or validation error.
        """

    def __init__(self, error: Error):
        location = [error.domain]
        message = error.message
        error_type = error.code
        super().__init__(loc=location, msg=message, type=error_type)


class DomainErrorResponse(ProblemDetail):
    """DomainErrorResponse

        HTTP ProblemDetail response for `DomainError`.

        Args:
            error: Domain error.
        """

    def __init__(self, error: DomainError):
        location = [error.domain]
        message = error.message
        module = error.__module__
        class_name = error.__class__.__name__
        error_type = f"{module}.{class_name}"
        super().__init__(loc=location, msg=message, type=error_type)
