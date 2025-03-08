import os

from pydantic import BaseModel


class Settings(BaseModel):
    mongodb_url: str = os.getenv(
        "MONGODB_URL", "mongodb://admin:password@mongodb:27017"
    )
    database_name: str = os.getenv(
        "DATABASE_NAME", "marcus_business"
    )  # marcus_business
    products_collection: str = "products"
    orders_collection: str = "orders"
    parts_collection: str = "parts"
    rules_collection: str = "configuration_rules"
    secret: str = "SECRET_KEY"
    jwt_token_lifetime: int = 3600
