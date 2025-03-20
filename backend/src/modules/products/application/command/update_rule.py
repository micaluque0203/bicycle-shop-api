from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import ConfigurationRule
from modules.products.domain.events import ConfigurationRuleUpdatedEvent
from modules.products.domain.repositories import ConfigurationRuleRepository
from modules.products.domain.value_objects import PartCategoryName


class UpdateConfigurationRuleCommand(Command):
    rule_id: PydanticObjectId
    depends_on: PartCategoryName
    depends_value: str
    forbidden_values: list[str]


async def update_configuration_rule_command(
    command: UpdateConfigurationRuleCommand, repository: ConfigurationRuleRepository
) -> CommandResult:
    rule = ConfigurationRule(
        _id=command.rule_id,
        depends_on=command.depends_on,
        depends_value=command.depends_value,
        forbidden_values=command.forbidden_values,
    )
    updated_rule = await repository.update(rule)

    event = ConfigurationRuleUpdatedEvent(
        rule_id=updated_rule.upserted_id,
        depends_on=rule.depends_on,
        depends_value=rule.depends_value,
        forbidden_values=rule.forbidden_values,
    )

    return CommandResult(entity_id=updated_rule.upserted_id, events=[event])
