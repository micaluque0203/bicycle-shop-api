from core.domain.value_objects import PydanticObjectId
from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.products.domain.aggregates import Product
from modules.products.domain.repositories import ProductRepository


class MongoDBProductRepository(
    MongoDBBaseRepository[PydanticObjectId, Product], ProductRepository
):
    def __init__(self, db) -> None:
        super().__init__(Product)
        self.db = db
        self.collection = self.db["products"]
