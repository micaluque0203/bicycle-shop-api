from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.aggregates import Product
from modules.products.domain.events import ProductCreatedEvent
from modules.products.domain.repositories import ProductRepository


class CreateProductCommand(Command):
    name: str
    category: str
    part_ids: list[PydanticObjectId]
    configuration_rule_ids: list[PydanticObjectId]


async def create_product_command(
    command: CreateProductCommand, repository: ProductRepository
) -> CommandResult:
    product = Product(
        name=command.name,
        category=command.category,
        part_ids=command.part_ids,
        configuration_rule_ids=command.configuration_rule_ids,
    )
    created_id = await repository.add(product)

    command = CommandResult(entity_id=created_id)
    return command.success(event=ProductCreatedEvent(product_id=created_id))
