from enum import Enum
from typing import Dict, List

from pydantic import BaseModel

from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import ConfigurationRule, Part
from modules.products.domain.value_objects import StockStatus


class OrderStatus(str, Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"


class OrderItem(BaseModel):
    product_id: PydanticObjectId
    configuration: List[Dict[str, str]]


ConfigurationOption = Dict[str, str]


class Configuration(BaseModel):
    """Order item configuration"""

    options: List[ConfigurationOption]

    def is_valid(self, rules: List[ConfigurationRule]) -> bool:

        options_dict = {
            list(option.keys())[0]: list(option.values())[0] for option in self.options
        }

        for rule in rules:
            if (
                rule.depends_on in options_dict
                and rule.depends_value == options_dict[rule.depends_on]
            ):
                if any(
                    forbidden in options_dict.values()
                    for forbidden in rule.forbidden_values
                ):
                    return False
        return True

    def is_in_stock(self, parts: List[Part]) -> bool:
        for option in self.options:
            part_type = list(option.keys())[0]
            part_name = list(option.values())[0]

            part_in_stock = any(
                part
                for part in parts
                if part.name == part_name
                and part.part_type == part_type
                and part.stock_status == StockStatus.AVAILABLE
            )

            print("PART IN STOCK", part_in_stock, part_type, part_name)

            if not part_in_stock:
                return False

        return True
