from typing import Coroutine

from core.domain.entities import Entity
from core.domain.value_objects import PydanticObjectId
from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.products.domain.repositories import ProductRepository


class MongoDBProductRepository(MongoDBBaseRepository, ProductRepository):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
        self.collection = self.db["products"]
