from typing import List

from pydantic import BaseModel, Field

from sharedkernel.domain.errors import Error, DomainError


class Request(BaseModel):
    """Request base class

    Serves as a formal agreement to interact with the API resources.
    """


class Response(BaseModel):
    """Response base class

    An API contract that defines as a standard HTTP response structure.
    """


class AckData(BaseModel):
    """Command Acknowledgement data

    Details Command and Resource specific data.

    Attributes:
        action: Name of the command executed.
        entity_id: Unique Identifier of the resource
        position: Number that represents the position of this change in the resource sequence of events
    """
    action: str
    entity_id: str = Field(alias="entityId")
    position: int


class AckResponse(Response):
    """Acknowledgement Response

    A response that communicates the status of command that has been executed.
    It indicates the position of state change in a particular resource after executing the action.

    Attributes:
        status: Status of the command executed on the request.
        data: Command and Resource specific data
    """
    status: str
    data: AckData


class ProblemDetail(Response):
    """ProblemDetail

    A standard machine-readable details of errors in an HTTP response.

    Attributes:
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
