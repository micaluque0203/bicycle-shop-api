from core.domain.value_objects import PydanticObjectId
from core.infrastructure.mongodb_base_repository import MongoDBBaseRepository
from modules.products.domain.entities import ConfigurationRule
from modules.products.domain.repositories import ConfigurationRuleRepository


class MongoDBConfigurationRulesRepository(
    MongoDBBaseRepository[PydanticObjectId, ConfigurationRule],
    ConfigurationRuleRepository,
):
    def __init__(self, db) -> None:
        super().__init__(ConfigurationRule)
        self.db = db
        self.collection = self.db["configuration_rules"]
