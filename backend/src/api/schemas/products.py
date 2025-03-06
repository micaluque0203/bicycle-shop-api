from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from modules.products.domain.entities import ConfigurationRule, Part


class ProductResponse(BaseModel):
    product_id: PydanticObjectId
    name: str
    category: str
    available_parts: List[Part] = []
    configuration_rules: List[ConfigurationRule] = []


class ProductCreatedResponse(BaseModel):
    product_id: PydanticObjectId
