from typing import Dict, List

from pydantic import BaseModel

from core.domain.value_objects import PydanticObjectId


class ValidateOrderItemRequest(BaseModel):
    product_id: PydanticObjectId
    configuration: List[Dict[str, str]]


class ValidateOrderItemResponse(BaseModel):
    is_valid: bool
