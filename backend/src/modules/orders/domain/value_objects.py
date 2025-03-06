from enum import Enum
from typing import Dict, List

from pydantic import BaseModel

from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import ConfigurationRule


class OrderStatus(Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"


class OrderItem(BaseModel):
    product_id: PydanticObjectId
    configuration: List[Dict[str, str]]


ConfigurationOption = Dict[str, str]


class Configuration(BaseModel):
    options: List[ConfigurationOption]

    def is_valid(self, rules: List[ConfigurationRule]) -> bool:

        options_dict = {
            list(option.keys())[0]: list(option.values())[0] for option in self.options
        }

        print("OPTIONS DICT", options_dict)
        print("rules", rules)

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
