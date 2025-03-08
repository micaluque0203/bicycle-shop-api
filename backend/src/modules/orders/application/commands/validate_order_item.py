from typing import List

from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.value_objects import Configuration
from modules.products.domain.entities import ConfigurationRule, Part
from modules.products.domain.repositories import (
    ConfigurationRuleRepository,
    PartRepository,
    ProductRepository,
)


class ValidateOrderItemCommand(Command):
    product_id: PydanticObjectId
    configuration: List[dict]


async def validate_order_item_command(
    command: ValidateOrderItemCommand,
    product_repository: ProductRepository,
    parts_repository: PartRepository,
    rules_repository: ConfigurationRuleRepository,
) -> CommandResult:
    product = await product_repository.get_by_id(command.product_id)
    if not product:
        return CommandResult.failure(f"Product {command.product_id} not found")

    config = Configuration(options=command.configuration)

    if "configuration_rule_ids" in product:
        config_rules = await rules_repository.find_all_by_id(
            filter={"$in": product["configuration_rule_ids"]}
        )
        if config.is_valid(config_rules) is False:
            return CommandResult.failure("Invalid configuration")

    product_parts = await parts_repository.find_all_by_id(
        filter={"$in": product["part_ids"]}
    )
    if not config.is_in_stock(product_parts):
        return CommandResult.failure("Some parts are not in stock")

    return CommandResult.success(
        payload={"is_valid": True},
    )
