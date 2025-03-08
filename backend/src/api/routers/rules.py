from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.auth import current_superuser
from api.infrastructure.client import get_rules_repository
from api.schemas.rules import ConfigurationRuleResponse
from core.domain.value_objects import PydanticObjectId
from modules.products.application.command.create_rule import (
    CreateConfigurationRuleCommand,
    create_configuration_rule_command,
)
from modules.products.application.command.delete_rule import (
    DeleteConfigurationRuleCommand,
    delete_configuration_rule_command,
)
from modules.products.application.command.update_rule import (
    UpdateConfigurationRuleCommand,
    update_configuration_rule_command,
)
from modules.products.application.query.get_rules_listing import (
    GetRulesListing,
    get_configuration_rules_listing,
)

router = APIRouter()


@router.post(
    "/admin/configuration-rules",
    response_model=ConfigurationRuleResponse,
    # dependencies=[Depends(current_superuser)],
)
async def create_configuration_rule(
    rule: CreateConfigurationRuleCommand, repository=Depends(get_rules_repository)
) -> ConfigurationRuleResponse:
    rule_created = await create_configuration_rule_command(rule, repository)
    return ConfigurationRuleResponse(id=rule_created.entity_id, **rule.model_dump())


@router.get(
    "/admin/configuration-rules",
    response_model=List[ConfigurationRuleResponse],
    # dependencies=[Depends(current_superuser)],
)
async def get_rules(
    repository=Depends(get_rules_repository),
) -> List[ConfigurationRuleResponse]:
    rules = await get_configuration_rules_listing(GetRulesListing(), repository)
    if not rules.payload:
        return []
    return rules.payload


@router.delete(
    "/admin/configuration-rules/{rule_id}",
    response_model=None,
    status_code=204,
    # dependencies=[Depends(current_superuser)],
)
async def delete_rule(
    rule_id: PydanticObjectId, repository=Depends(get_rules_repository)
):
    await delete_configuration_rule_command(
        DeleteConfigurationRuleCommand(rule_id=rule_id), repository
    )


@router.put(
    "/admin/configuration-rules/{rule_id}",
    response_model=ConfigurationRuleResponse,
    status_code=200,
    # dependencies=[Depends(current_superuser)],
)
async def update_rule(
    rule: UpdateConfigurationRuleCommand, repository=Depends(get_rules_repository)
):
    result = await update_configuration_rule_command(rule, repository)
    if result.has_errors:
        raise HTTPException(status_code=404, detail=result.error)

    if result.is_success() and result.events:
        return result.events[0].model_dump()
