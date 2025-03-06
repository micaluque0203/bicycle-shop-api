from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.events import ProductDeletedEvent
from modules.products.domain.repositories import ProductRepository


class DeleteProductCommand(Command):
    product_id: PydanticObjectId


async def delete_product_command(
    command: DeleteProductCommand, repository: ProductRepository
) -> CommandResult:
    # TODO: get and check rules before deleting
    deleted_count = await repository.remove(command.product_id)
    if deleted_count == 0:
        return CommandResult.error(f"Product with id {command.product_id} not found")
    return CommandResult.success(
        event=ProductDeletedEvent(product_id=command.product_id)
    )
