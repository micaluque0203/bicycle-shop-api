from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.entities import Part
from modules.products.domain.events import PartUpdatedEvent
from modules.products.domain.repositories import PartRepository
from modules.products.domain.value_objects import PartCategoryName, StockStatus


class UpdatePartCommand(Command):
    part_id: PydanticObjectId
    part_type: PartCategoryName
    name: str
    stock_status: str = StockStatus.AVAILABLE


async def update_part_command(
    command: UpdatePartCommand, repository: PartRepository
) -> CommandResult:
    part = Part(
        _id=command.part_id,
        part_type=command.part_type,
        name=command.name,
        stock_status=command.stock_status,
    )
    updated_part = await repository.update(part)

    event = PartUpdatedEvent(part_id=updated_part.upserted_id)
    return CommandResult(entity_id=updated_part.upserted_id, events=[event])
