from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.modules.orders.application.commands.validate_order_item import (
    ValidateOrderItemCommand, validate_order_item_command)
from src.modules.orders.domain.repositories import OrderRepository
from src.modules.products.domain.aggregates import Product
from src.modules.products.domain.entities import ConfigurationRule, Part
from src.modules.products.domain.repositories import (
    ConfigurationRuleRepository, PartRepository, ProductRepository)
from src.modules.products.domain.value_objects import (PartCategoryName,
                                                       StockStatus)


@pytest.fixture
def product_exists():
    return {
        "id": ObjectId("67caa7d400be092083bf2e5c"),
        "events": [],
        "name": "Custom Bicycle",
        "category": "Bikes",
        "part_ids": [],
        "configuration_rule_ids": [
            ObjectId("67caa7d400be092083bf2e5a"),
            ObjectId("67caa7d400be092083bf2e5b"),
        ],
    }


@pytest.fixture
def parts_in_stock():
    return [
        Part(
            id=ObjectId(),
            name="Full-suspension",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            id=ObjectId(),
            name="Road wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            id=ObjectId(),
            name="Blue",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]


@pytest.mark.asyncio
async def test_validate_order_item_command_is_valid_is_in_stock(
    product_exists, parts_in_stock
):

    command = ValidateOrderItemCommand(
        product_id=product_exists["id"],
        configuration=[
            {PartCategoryName.FRAME: "Full-suspension"},
            {PartCategoryName.WHEELS: "Road wheels"},
            {PartCategoryName.RIM_COLOR: "Blue"},
        ],
    )

    product_repository = AsyncMock(spec=ProductRepository)
    product_repository.get_by_id = AsyncMock()
    product_repository.get_by_id.return_value = product_exists

    parts_repository = AsyncMock(spec=PartRepository)
    parts_repository.find_all_by_id = AsyncMock()
    parts_repository.find_all_by_id.return_value = parts_in_stock

    rules_repository = AsyncMock(spec=ConfigurationRuleRepository)
    rules_repository.find_all_by_id = AsyncMock()
    rules_repository.find_all_by_id.return_value = [
        ConfigurationRule(
            depends_on=PartCategoryName.FRAME,
            depends_value="Full-suspension",
            forbidden_values=["red"],
        )
    ]

    result = await validate_order_item_command(
        command, product_repository, parts_repository, rules_repository
    )

    assert result.payload == {"is_valid": True}


@pytest.mark.asyncio
async def test_validate_order_item_product_not_found(parts_in_stock):
    random_id = ObjectId()
    command = ValidateOrderItemCommand(
        product_id=random_id,
        configuration=[
            {PartCategoryName.FRAME: "full-suspension"},
            {PartCategoryName.WHEELS: "road wheels"},
            {PartCategoryName.RIM_COLOR: "blue"},
        ],
    )

    product_repository = AsyncMock(spec=ProductRepository)
    product_repository.get_by_id = AsyncMock()
    product_repository.get_by_id.return_value = None

    parts_repository = AsyncMock(spec=PartRepository)
    parts_repository.find_all_by_id = AsyncMock()
    parts_repository.find_all_by_id.return_value = parts_in_stock

    rules_repository = AsyncMock(spec=ConfigurationRuleRepository)
    rules_repository.find_all_by_id = AsyncMock()
    rules_repository.find_all_by_id.return_value = [
        ConfigurationRule(
            depends_on=PartCategoryName.FRAME,
            depends_value="full-suspension",
            forbidden_values=["red"],
        )
    ]

    result = await validate_order_item_command(
        command, product_repository, parts_repository, rules_repository
    )

    assert f"Product {str(random_id)} not found" in result.errors[0]


@pytest.mark.asyncio
async def test_validate_order_item_invalid_configuration(
    product_exists, parts_in_stock
):
    command = ValidateOrderItemCommand(
        product_id=product_exists["id"],
        configuration=[
            {PartCategoryName.FRAME: "diamond"},
            {PartCategoryName.WHEELS: "mountain wheels"},
            {PartCategoryName.RIM_COLOR: "red"},
        ],
    )

    product_repository = AsyncMock(spec=ProductRepository)
    product_repository.get_by_id = AsyncMock()
    product_repository.get_by_id.return_value = product_exists

    parts_repository = AsyncMock(spec=PartRepository)
    parts_repository.find_all_by_id = AsyncMock()
    parts_repository.find_all_by_id.return_value = parts_in_stock

    rules_repository = AsyncMock(spec=ConfigurationRuleRepository)
    rules_repository.find_all_by_id = AsyncMock()
    rules_repository.find_all_by_id.return_value = [
        ConfigurationRule(
            depends_on=PartCategoryName.WHEELS,
            depends_value="mountain wheels",
            forbidden_values=["diamond", "step-through"],
        ),
        ConfigurationRule(
            depends_on=PartCategoryName.WHEELS,
            depends_value="fat bike wheels",
            forbidden_values=["red"],
        ),
    ]

    result = await validate_order_item_command(
        command, product_repository, parts_repository, rules_repository
    )
    assert "Invalid configuration" in result.errors[0]


@pytest.mark.asyncio
async def test_validate_order_item_part_out_of_stock(product_exists):
    command = ValidateOrderItemCommand(
        product_id=product_exists["id"],
        configuration=[
            {PartCategoryName.FRAME: "diamond"},
            {PartCategoryName.WHEELS: "Road wheels"},
            {PartCategoryName.RIM_COLOR: "red"},
        ],
    )

    product_repository = AsyncMock(spec=ProductRepository)
    product_repository.get_by_id = AsyncMock()
    product_repository.get_by_id.return_value = product_exists

    parts_repository = AsyncMock(spec=PartRepository)
    parts_repository.find_all_by_id = AsyncMock()
    parts_repository.find_all_by_id.return_value = [
        Part(
            id=ObjectId(),
            name="diamond",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            id=ObjectId(),
            name="Road wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.OUT_OF_STOCK,
        ),
        Part(
            id=ObjectId(),
            name="red",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]

    rules_repository = AsyncMock(spec=ConfigurationRuleRepository)
    rules_repository.find_all_by_id = AsyncMock()
    rules_repository.find_all_by_id.return_value = [
        ConfigurationRule(
            depends_on=PartCategoryName.WHEELS,
            depends_value="mountain wheels",
            forbidden_values=["diamond", "step-through"],
        ),
        ConfigurationRule(
            depends_on=PartCategoryName.WHEELS,
            depends_value="fat bike wheels",
            forbidden_values=["red"],
        ),
    ]

    result = await validate_order_item_command(
        command, product_repository, parts_repository, rules_repository
    )
    assert "Some parts are not in stock" in result.errors[0]
