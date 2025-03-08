from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.aggregates import Product
from modules.products.domain.events import ProductUpdatedEvent
from modules.products.domain.repositories import ProductRepository


class UpdateProductCommand(Command):
    product_id: PydanticObjectId
    name: str
    category: str
    part_ids: list[PydanticObjectId]
    configuration_rule_ids: list[PydanticObjectId]


async def update_product_command(
    command: UpdateProductCommand, repository: ProductRepository
) -> CommandResult:
    product = Product(
        id=command.product_id,
        name=command.name,
        category=command.category,
        part_ids=command.part_ids,
        configuration_rule_ids=command.configuration_rule_ids,
    )
    updated_product = await repository.update(product)
    event = ProductUpdatedEvent(product_id=updated_product.upserted_id)
    return CommandResult(entity_id=updated_product.upserted_id, events=[event])
