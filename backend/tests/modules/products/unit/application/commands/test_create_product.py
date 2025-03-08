from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.create_product import (
    CreateProductCommand, create_product_command)
from src.modules.products.domain.repositories import ProductRepository


@pytest.mark.asyncio
async def test_create_product_command():
    expected_id = ObjectId()

    command = CreateProductCommand(
        name="Test Product",
        category="Test Category",
        part_ids=[],
        configuration_rule_ids=[],
    )

    repository = AsyncMock(spec=ProductRepository)
    repository.add = AsyncMock()
    repository.add.return_value = expected_id
    result = await create_product_command(command, repository)

    assert result.success
    assert result.events[0].product_id == expected_id
