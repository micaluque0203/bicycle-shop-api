from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.delete_product import (
    DeleteProductCommand, delete_product_command)
from src.modules.products.domain.repositories import ProductRepository


@pytest.mark.asyncio
async def test_delete_product_command():
    expected_id = ObjectId()

    command = DeleteProductCommand(
        product_id=expected_id,
    )

    repository = AsyncMock(spec=ProductRepository)
    repository.remove = AsyncMock()
    repository.remove.return_value = expected_id
    result = await delete_product_command(command, repository)

    assert result.success
    assert result.events[0].product_id == expected_id
