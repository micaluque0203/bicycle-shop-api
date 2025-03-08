from typing import List

from core.domain.entities import Aggregate
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.value_objects import Configuration
from modules.products.domain.entities import ConfigurationRule, Part
from modules.products.domain.value_objects import PartCategoryName


class Product(Aggregate):
    name: str
    category: str
    part_ids: List[PydanticObjectId] = []
    configuration_rule_ids: List[PydanticObjectId] = []

    def is_configuration_allowed(
        self, configuration: Configuration, rules: List[ConfigurationRule]
    ) -> bool:
        rules
        product_rules = [
            rule for rule in rules if rule.id in self.configuration_rule_ids
        ]
        return configuration.is_valid(product_rules)
