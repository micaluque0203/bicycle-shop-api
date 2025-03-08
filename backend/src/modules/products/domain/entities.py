from typing import List

from core.domain.entities import Entity
from modules.products.domain.value_objects import PartCategoryName, StockStatus


class ConfigurationRule(Entity):
    depends_on: PartCategoryName
    depends_value: str
    forbidden_values: List[str]


class Part(Entity):
    part_type: PartCategoryName
    name: str
    stock_status: StockStatus = StockStatus.AVAILABLE

    def is_available(self) -> bool:
        return self.stock_status == StockStatus.AVAILABLE
