from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class ConfigurationRuleResponse(BaseModel):
    rule_id: PydanticObjectId = Field(alias="id")
    depends_on: str
    depends_value: str
    forbidden_values: List[str]


class ConfigurationRuleUpdateResponse(BaseModel):
    rule_id: PydanticObjectId = Field(alias="id")


class UpdateConfigurationRuleRequest(BaseModel):
    depends_on: str
    depends_value: str
    forbidden_values: List[str]
