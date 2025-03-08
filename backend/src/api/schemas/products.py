from typing import List

from pydantic import BaseModel

from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import ConfigurationRule, Part


class ProductResponse(BaseModel):
    product_id: PydanticObjectId
    name: str
    category: str
    available_parts: List[Part] = []
    configuration_rules: List[ConfigurationRule] = []


class ProductCreatedResponse(BaseModel):
    product_id: PydanticObjectId


class UpdateProductRequest(BaseModel):
    name: str
    category: str
    part_ids: List[PydanticObjectId]
    configuration_rule_ids: List[PydanticObjectId]
