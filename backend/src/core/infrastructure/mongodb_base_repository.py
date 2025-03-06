from core.domain.entities import Entity
from core.domain.repositories import GenericRepository
from core.domain.value_objects import PydanticObjectId


class MongoDBBaseRepository(GenericRepository[PydanticObjectId, Entity]):
    def __init__(self) -> None:
        super().__init__()

    async def remove(self, entity_id: PydanticObjectId) -> int:
        product = await self.collection.delete_one({"_id": entity_id})
        return product.deleted_count

    async def get_by_id(self, entity_id: PydanticObjectId) -> Entity:
        product = await self.collection.find_one({"_id": entity_id})
        return product

    async def find_all_by_id(self, filter: dict) -> Entity:
        products = await self.collection.find({"_id": filter}).to_list()
        return products

    async def add(self, entity: Entity) -> PydanticObjectId:
        document = await self.collection.insert_one(
            entity.model_dump(exclude_none=True, exclude={"id"})
        )
        return document.inserted_id

    async def get_all(self) -> list[Entity]:
        products = await self.collection.find().to_list()
        return products

    async def update(self, entity: Entity) -> list[Entity]:
        updated_entity = await self.collection.update_one(
            {"_id": entity.id},
            {"$set": entity.model_dump(exclude_none=True, exclude={"id"})},
        )
        return updated_entity
