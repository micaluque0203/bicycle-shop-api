from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.auth import current_superuser
from api.infrastructure.client import get_rules_repository
from modules.products.application.command.create_rule import (
    CreateConfigurationRuleCommand, create_configuration_rule_command)
from modules.products.application.query.get_rules_listing import (
    GetRulesListing, get_configuration_rules_listing)
from modules.products.domain.entities import ConfigurationRule

router = APIRouter()


@router.post(
    "/admin/configuration-rules",
    response_model=ConfigurationRule,
    dependencies=[Depends(current_superuser)],
)
async def create_configuration_rule(
    rule: CreateConfigurationRuleCommand, repository=Depends(get_rules_repository)
):
    rule_created = await create_configuration_rule_command(rule, repository)
    return ConfigurationRule(id=rule_created.entity_id, **rule.model_dump())


@router.get(
    "/admin/configuration-rules",
    response_model=List[ConfigurationRule],
    dependencies=[Depends(current_superuser)],
)  # TODO: add Response Model
async def get_rules(repository=Depends(get_rules_repository)):
    rules = await get_configuration_rules_listing(GetRulesListing(), repository)
    if not rules.payload:
        return []
    return rules.payload


# @router.delete(
#     "/admin/configuration-rules/{rule_id}",
#     response_model=ConfigurationRule,
#     dependencies=[Depends(current_superuser)],
# )
# async def delete_configuration_rule(
#     rule_id: PydanticObjectId, repository=Depends(get_rules_repository)
# ):
#     await delete_rule_configuration_command(
#         DeleteRuleConfigurationCommand(rule_id=rule_id), repository
#     )


# @router.put(
#     "/admin/products/{product_id}/configuration-rules",
#     response_model=Product,
#     dependencies=[Depends(current_superuser)],
# )
# async def update_product_configuration_rules(product_id: str, rule_ids: List[str]):
#     modified_count = repo.update_product_rules(product_id, rule_ids)
#     if modified_count == 0:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"updated": True}
