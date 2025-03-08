from dataclasses import dataclass

from core.application.commands import Command, CommandResult
from modules.products.domain.entities import ConfigurationRule
from modules.products.domain.events import ConfigurationRuleCreatedEvent
from modules.products.domain.repositories import PartRepository
from modules.products.domain.value_objects import PartCategoryName


class CreateConfigurationRuleCommand(Command):
    depends_on: PartCategoryName
    depends_value: str
    forbidden_values: list[str]


async def create_configuration_rule_command(
    command: CreateConfigurationRuleCommand, repository: PartRepository
) -> CommandResult:

    rule = ConfigurationRule(
        depends_on=command.depends_on,
        depends_value=command.depends_value,
        forbidden_values=command.forbidden_values,
    )

    created_rule = await repository.add(rule)
    return CommandResult.success(
        event=ConfigurationRuleCreatedEvent(rule_id=created_rule)
    )
