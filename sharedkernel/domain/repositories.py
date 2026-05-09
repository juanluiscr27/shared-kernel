from abc import ABC
from typing import Any

from typeinspection.handlers import get_super_name

from sharedkernel.domain.models import Entity


class Repository[TEntity: Entity[Any]](ABC):
    """Repository Generic Abstract Base class

    The Repository Interface defines the operations to manage data access logic in a centralized location.
    It separates the logic of saving and retrieving the data from the business logic and maps it to the entity model.

    Classes based on this generic abstract repository should implement the methods to `save`, `find_by_id`,
    `find_by_slug` and `find_all` entity of type `TEntity`.
    """

    @property
    def aggregate_type(self) -> str:
        """Returns the qualified name of the entity this repository is based on"""
        return get_super_name(self)

    # def save(self, entity: TEntity) -> None:
    #     """Saves or updates an entity of type TEntity.
    #
    #     Args:
    #         entity: The entity to save.
    #     """
    #
    # @abstractmethod
    # def add(self, entity: TEntity) -> None:
    #     """Store an entity and leaves the transaction open.
    #
    #     Args:
    #         entity: The entity to save.
    #     """
    #
    # def get(self, entity_id: UUID) -> TEntity:
    #     """Gets an entity by its unique identifier.
    #
    #     Args:
    #         entity_id: The identifier.
    #
    #     Returns:
    #         The found entity.
    #
    #     Raises:
    #         EntityNotFound: If the identifier is not associated to any Entity in the repository.
    #     """
    #
    # def find_by_id(self, entity_id: UUID) -> Optional[TEntity]:
    #     """Finds an entity by its unique identifier.
    #
    #     Args:
    #         entity_id: The unique identifier.
    #
    #     Returns:
    #         The found entity or None.
    #     """
    #
    # def find_by_slug(self, slug: str) -> Optional[TEntity]:
    #     """Finds an entity by its human-readable slug.
    #
    #     Args:
    #         slug: The slug identifier.
    #
    #     Returns:
    #         The found entity or None.
    #     """
    #
    # def find_all(self) -> List[TEntity]:
    #     """Retrieves all entities of type TEntity.
    #
    #     Returns:
    #         A list of entities.
    #     """


class ReadRepository(ABC):
    """Repository Abstract Base class for `ReadModel` objects

    This abstract class is a Facade that provides a simplified interface to retrieve data models optimized for reads.

    Classes based on this abstract repository should implement the methods to `get_by_id`, `get_by_slug` and
    `get_all` data models of a given type.
    """
    # def get_by_id(self, entity_id: UUID) -> ReadModel:
    #     """Gets a read model by its identifier.
    #
    #     Args:
    #         entity_id: The identifier.
    #
    #     Returns:
    #         The found read model details.
    #
    #     Raises:
    #         EntityNotFound: If the identifier is not associated to any ReadModel in the repository.
    #     """
    #
    # def get_by_slug(self, slug: str) -> ReadModel:
    #     """Gets a read model by its slug.
    #
    #     Args:
    #         slug: The slug.
    #
    #     Returns:
    #         The found read model details.
    #
    #     Raises:
    #         EntityNotFound: If the slug is not associated to any ReadModel in the repository.
    #     """
    #
    # def get_all(self) -> List[ReadModel]:
    #     """Retrieves all read models handled by this repository.
    #
    #     Returns:
    #         A list of read models.
    #     """
