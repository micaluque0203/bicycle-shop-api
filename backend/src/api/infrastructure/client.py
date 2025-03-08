from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from api.settings import Settings
from modules.iam.domain.entities import User
from modules.orders.infrastructure.orders_repository import MongoDBOrdersRepository
from modules.products.infrastructure.parts_repository import MongoDBPartsRepository
from modules.products.infrastructure.product_repository import MongoDBProductRepository
from modules.products.infrastructure.rules_repository import (
    MongoDBConfigurationRulesRepository,
)


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def __aenter__(self):
        self.settings = Settings()
        self.client = AsyncIOMotorClient(self.settings.mongodb_url)
        self.db = self.client[self.settings.database_name]
        ## await self.init_db()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    async def init_db(self):
        if self.db is not None:

            await init_beanie(database=self.db, document_models=[User])
        else:
            raise Exception("Database is not initialized")

    async def get_database(self):
        if self.db is None:
            await self.__aenter__()
        return self.db


mongodb_instance = MongoDB()


async def get_mongodb():
    async with mongodb_instance as db:
        yield await db.get_database()


async def get_repository(repository_class):
    async for db in get_mongodb():
        yield repository_class(db)


async def get_orders_repository():
    async for repo in get_repository(MongoDBOrdersRepository):
        yield repo


async def get_parts_repository():
    async for repo in get_repository(MongoDBPartsRepository):
        yield repo


async def get_products_repository():
    async for repo in get_repository(MongoDBProductRepository):
        yield repo


async def get_rules_repository():
    async for repo in get_repository(MongoDBConfigurationRulesRepository):
        yield repo
