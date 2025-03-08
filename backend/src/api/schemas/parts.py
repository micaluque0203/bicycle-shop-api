from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from modules.products.domain.value_objects import PartCategoryName, StockStatus


class PartResponse(BaseModel):
    part_id: PydanticObjectId = Field(alias="id")
    part_type: PartCategoryName
    name: str
    stock_status: StockStatus
