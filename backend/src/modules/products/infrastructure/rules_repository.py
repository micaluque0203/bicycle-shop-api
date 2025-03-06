from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.products.domain.repositories import ConfigurationRuleRepository


class MongoDBConfigurationRulesRepository(
    MongoDBBaseRepository, ConfigurationRuleRepository
):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
        self.collection = self.db["configuration_rules"]
