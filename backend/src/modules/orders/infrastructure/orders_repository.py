from core.domain.value_objects import PydanticObjectId
from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.orders.domain.aggregates import Order
from modules.orders.domain.repositories import OrderRepository


class MongoDBOrdersRepository(MongoDBBaseRepository, OrderRepository):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
        self.collection = self.db["orders"]

    async def get_by_user_id(self, user_id: PydanticObjectId) -> Order:
        response = await self.collection.find_one({"user_id": user_id})
        return Order(**response) if response else None
