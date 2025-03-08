from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.delete_part import (
    DeletePartCommand, delete_part_command)
from src.modules.products.domain.events import PartDeletedEvent
from src.modules.products.domain.repositories import PartRepository


@pytest.mark.asyncio
async def test_delete_part_command():
    expected_id = ObjectId()

    command = DeletePartCommand(
        part_id=expected_id,
    )

    repository = AsyncMock(spec=PartRepository)
    repository.remove = AsyncMock()
    repository.remove.return_value = expected_id
    result = await delete_part_command(command, repository)

    assert result.success
    assert result.events[0].part_id == expected_id
