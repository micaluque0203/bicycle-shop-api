from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.create_part import (
    CreatePartCommand,
    create_part_command,
)
from src.modules.products.domain.repositories import PartRepository
from src.modules.products.domain.value_objects import PartCategoryName, StockStatus


@pytest.mark.asyncio
async def test_create_part_command():
    expected_id = ObjectId()

    command = CreatePartCommand(
        part_type=PartCategoryName.FRAME,
        name="diamond",
        stock_status=StockStatus.AVAILABLE,
    )

    repository = AsyncMock(spec=PartRepository)
    repository.add = AsyncMock()
    repository.add.return_value = expected_id
    result = await create_part_command(command, repository)

    assert result.success
    assert result.events[0].part_id == expected_id
