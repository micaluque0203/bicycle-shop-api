from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.events import PartDeletedEvent
from modules.products.domain.repositories import PartRepository


class DeletePartCommand(Command):
    part_id: PydanticObjectId


async def delete_part_command(
    command: DeletePartCommand, repository: PartRepository
) -> CommandResult:
    # TODO: get and check rules before deleting
    deleted_count = await repository.remove(command.part_id)
    if deleted_count == 0:
        return CommandResult.error(f"Part with id {command.part_id} not found")
    return CommandResult.success(event=PartDeletedEvent(part_id=command.part_id))
