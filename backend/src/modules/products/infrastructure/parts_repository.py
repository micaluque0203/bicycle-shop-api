from core.domain.value_objects import PydanticObjectId
from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.products.domain.entities import Part
from modules.products.domain.repositories import PartRepository


class MongoDBPartsRepository(
    MongoDBBaseRepository[PydanticObjectId, Part], PartRepository
):
    def __init__(self, db) -> None:
        super().__init__(Part)
        self.db = db
        self.collection = self.db["parts"]
