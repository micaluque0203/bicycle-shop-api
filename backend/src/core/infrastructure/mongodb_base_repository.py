from typing import List, Type, TypeVar

from pydantic import BaseModel

from core.domain.entities import Entity
from core.domain.repositories import GenericRepository
from core.domain.value_objects import PydanticObjectId

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=PydanticObjectId)


class MongoDBBaseRepository(GenericRepository[ID, T]):
    def __init__(self, entity_class: Type[T]) -> None:
        super().__init__()
        self.entity_class = entity_class

    async def remove(self, entity_id: PydanticObjectId) -> int:
        product = await self.collection.delete_one({"_id": entity_id})
        return product.deleted_count

    async def get_by_id(self, entity_id: PydanticObjectId) -> T:
        product = await self.collection.find_one({"_id": entity_id})
        return product

    async def find_all_by_id(self, filter: dict) -> List[T]:
        documents = await self.collection.find({"_id": filter}).to_list()
        return [self.entity_class(**document) for document in documents]

    async def add(self, entity: T) -> PydanticObjectId:
        document = await self.collection.insert_one(
            entity.model_dump(exclude_none=True, exclude={"id"})
        )
        return document.inserted_id

    async def get_all(self) -> list[T]:
        documents = await self.collection.find().to_list()
        return [self.entity_class(**document) for document in documents]

    async def update(self, entity: T) -> T:
        updated_entity = await self.collection.update_one(
            {"_id": entity.id},
            {"$set": entity.model_dump(exclude_none=True, exclude={"id"})},
        )
        return updated_entity
