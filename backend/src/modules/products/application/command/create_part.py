from dataclasses import dataclass

from core.application.commands import Command, CommandResult
from modules.products.domain.entities import Part
from modules.products.domain.events import PartCreatedEvent
from modules.products.domain.repositories import PartRepository
from modules.products.domain.value_objects import PartCategoryName, StockStatus


@dataclass
class CreatePartCommand(Command):
    part_type: PartCategoryName
    name: str
    stock_status: str = StockStatus.AVAILABLE


async def create_part_command(
    command: CreatePartCommand, repository: PartRepository
) -> CommandResult:
    part = Part(
        part_type=command.part_type,
        name=command.name,
        stock_status=command.stock_status,
    )

    await repository.add(part)
    return CommandResult.success(event=PartCreatedEvent(part_id=part.id))
