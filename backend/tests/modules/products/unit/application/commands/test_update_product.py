from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.update_product import (
    UpdateProductCommand,
    update_product_command,
)
from src.modules.products.domain.aggregates import Product
from src.modules.products.domain.repositories import ProductRepository


@pytest.mark.asyncio
async def test_update_product_command():
    expected_id = ObjectId("67c9f0847fa8e0ace06e3bd4")

    command = UpdateProductCommand(
        product_id=expected_id,
        name="Test Product",
        category="Test Category",
        part_ids=[],
        configuration_rule_ids=[],
    )

    repository = AsyncMock(spec=ProductRepository)
    repository.update = AsyncMock()
    expected_product = Product(
        _id=expected_id,
        name="Test Product",
        category="Test Category",
        part_ids=[],
        configuration_rule_ids=[],
    )
    repository.update.return_value = expected_product

    result = await update_product_command(command, repository)

    assert result.is_success
    assert result.entity_id == expected_id
