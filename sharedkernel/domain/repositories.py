from abc import ABC


class Repository(ABC):
    """Repository Abstract Base class

    The Repository Interface defines the operations to manage data access logic in a centralized location.
    It separates the logic of saving and retrieving the data from the business logic and maps it to the entity model.
    """


class ReadRepository(ABC):
    """Repository Abstract Base class for `ReadModel` objects

    This abstract class is Facade that provides a simplified interface to retrieve data models optimized for reads.
    """
