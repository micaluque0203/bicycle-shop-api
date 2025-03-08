from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.products.application.command.create_rule import (
    CreateConfigurationRuleCommand,
    create_configuration_rule_command,
)
from src.modules.products.domain.repositories import ConfigurationRuleRepository
from src.modules.products.domain.value_objects import PartCategoryName


@pytest.mark.asyncio
async def test_create_rule_command():
    expected_id = ObjectId()

    command = CreateConfigurationRuleCommand(
        depends_on=PartCategoryName.FRAME,
        depends_value="depends_value",
        forbidden_values=["forbidden_values"],
    )

    repository = AsyncMock(spec=ConfigurationRuleRepository)
    repository.add = AsyncMock()
    repository.add.return_value = expected_id
    result = await create_configuration_rule_command(command, repository)

    assert result.success
    assert result.events[0].rule_id == expected_id
