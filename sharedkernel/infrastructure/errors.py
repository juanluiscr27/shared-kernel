class MapperNotFound(Exception):
    """MapperNotFound Error

    Raised when no `EventMapper` was found in the `MappingPipeline` for a given event type.

    Args:
        event_type: Entity on which the error was raised.
    """

    def __init__(self, event_type: str):
        message = f"No Event Mapper was found for event {event_type}."
        super().__init__(message)
