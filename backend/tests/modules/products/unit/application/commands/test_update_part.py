from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.update_part import (
    UpdatePartCommand, update_part_command)
from src.modules.products.domain.entities import Part
from src.modules.products.domain.repositories import PartRepository
from src.modules.products.domain.value_objects import (PartCategoryName,
                                                       StockStatus)


@pytest.mark.asyncio
async def test_update_part_command():
    expected_id = ObjectId("67c9f0847fa8e0ace06e3bd4")

    command = UpdatePartCommand(
        part_id=expected_id,
        part_type=PartCategoryName.CHAIN,
        name="Test Part",
        stock_status=StockStatus.OUT_OF_STOCK,
    )

    repository = AsyncMock(spec=PartRepository)
    repository.update = AsyncMock()
    expected_part = Part(
        id=expected_id,
        part_type=PartCategoryName.CHAIN,
        name="Test Part",
        stock_status=StockStatus.OUT_OF_STOCK,
    )
    repository.update.return_value = expected_part

    result = await update_part_command(command, repository)

    assert result.is_success
    assert result.entity_id == expected_part.id
