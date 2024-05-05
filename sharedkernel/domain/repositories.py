import typing
from abc import ABC
from types import get_original_bases
from typing import Generic, TypeVar

from sharedkernel.domain.models import Entity

TEntity = TypeVar("TEntity", bound=Entity)


class Repository(ABC, Generic[TEntity]):
    """Repository Generic Abstract Base class

    The Repository Interface defines the operations to manage data access logic in a centralized location.
    It separates the logic of saving and retrieving the data from the business logic and maps it to the entity model.

    Classes based on this generic abstract repository should implement the methods to `save`, `find_by_id`,
    `find_by_slug` and `find_all` entity of type `TEntity`.
    """

    @property
    def aggregate_type(self) -> str:
        """Returns the fully qualified name of the entity this repository is based on"""
        bases = get_original_bases(self.__class__)
        args = typing.get_args(bases[0])
        module = args[0].__module__
        class_name = args[0].__name__
        return f"{module}.{class_name}"

    # save (self, entity: TEntity):

    # find_by_id(self, entity_id: TId) -> Optional[TEntity]:

    # find_by_slug(self, slug: str) -> Optional[TEntity]:

    # find_all(self) -> List[TEntity]:


class ReadRepository(ABC):
    """Repository Abstract Base class for `ReadModel` objects

    This abstract class is a Facade that provides a simplified interface to retrieve data models optimized for reads.

    Classes based on this abstract repository should implement the methods to `find_by_id`, `find_by_slug` and
    `find_all` data models of a given type.
    """
    # find_by_id(self, official_id: UUID) -> Optional[OfficialDetails]:

    # find_by_slug(self, slug: str) -> Optional[OfficialDetails]:

    # find_all(self) -> List[OfficialDetails]:
