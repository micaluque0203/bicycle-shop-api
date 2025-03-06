from typing import List

from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.value_objects import Configuration, OrderItem
from modules.products.domain.entities import ConfigurationRule
from modules.products.domain.repositories import ProductRepository


class ValidateOrderItemCommand(Command):
    product_id: PydanticObjectId
    configuration: List[dict]


async def validate_order_item_command(
    command: ValidateOrderItemCommand, product_repository: ProductRepository
) -> CommandResult:
    product = await product_repository.get_by_id(command.product_id)
    if not product:
        return CommandResult.failure(f"Product {command.product_id} not found")

    if "configuration_rules" in product:
        rules = [ConfigurationRule(**rule) for rule in product["configuration_rules"]]

        config = Configuration(options=command.configuration)

        if not config.is_valid(rules):
            return CommandResult.failure("Invalid configuration")

    return CommandResult.success(
        payload={"is_valid": True},
    )
