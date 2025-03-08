import abc
from typing import Generic, TypeVar

from core.domain.entities import Entity
from core.domain.value_objects import PydanticObjectId

T = TypeVar("T", bound=Entity)
EntityId = TypeVar("EntityId", bound=PydanticObjectId)


class GenericRepository(Generic[EntityId, T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, entity: T):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: T):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: EntityId) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all_by_id(self, filter: dict) -> list[T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError()
