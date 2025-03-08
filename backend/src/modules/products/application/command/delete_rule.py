from dataclasses import dataclass

from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import ConfigurationRule
from modules.products.domain.events import ConfigurationRuleDeletedEvent
from modules.products.domain.repositories import ConfigurationRuleRepository
from modules.products.domain.value_objects import PartCategoryName


class DeleteConfigurationRuleCommand(Command):
    rule_id: PydanticObjectId


async def delete_configuration_rule_command(
    command: DeleteConfigurationRuleCommand, repository: ConfigurationRuleRepository
) -> CommandResult:

    deleted_count = await repository.remove(command.rule_id)
    if deleted_count == 0:
        return CommandResult.error(
            f"Configuration Rule with id {command.rule_id} not found"
        )
    return CommandResult.success(
        event=ConfigurationRuleDeletedEvent(rule_id=command.rule_id)
    )
