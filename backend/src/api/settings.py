from pydantic import BaseModel


class Settings(BaseModel):
    mongodb_url: str = "mongodb://admin:password@127.0.0.1:27017"
    database_name: str = "marcus_business"
    products_collection: str = "products"
    orders_collection: str = "orders"
    parts_collection: str = "parts"
    rules_collection: str = "configuration_rules"
    secret: str = "SECRET_KEY"
    jwt_token_lifetime: int = 3600


settings = Settings()
