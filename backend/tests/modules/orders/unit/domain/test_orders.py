from bson import ObjectId

from src.modules.orders.domain.aggregates import Order
from src.modules.orders.domain.value_objects import Configuration, OrderStatus
from src.modules.products.domain.aggregates import Configuration, Product
from src.modules.products.domain.entities import ConfigurationRule, Part
from src.modules.products.domain.value_objects import (PartCategoryName,
                                                       StockStatus)


def test_dynamic_configuration_validation():
    rules = [
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
    valid_config = Configuration(
        options=[
            {PartCategoryName.FRAME: "full-suspension"},
            {PartCategoryName.WHEELS: "mountain wheels"},
            {PartCategoryName.RIM_COLOR: "black"},
        ]
    )
    invalid_config = Configuration(
        options=[
            {PartCategoryName.FRAME: "diamond"},
            {PartCategoryName.WHEELS: "mountain wheels"},
            {PartCategoryName.RIM_COLOR: "red"},
        ]
    )

    assert valid_config.is_valid(rules) == True
    assert invalid_config.is_valid(rules) == False


def test_order_valid_fullfiled():
    config = Configuration(
        options=[
            {PartCategoryName.FRAME: "full-suspension"},
            {PartCategoryName.WHEELS: "road wheels"},
            {PartCategoryName.RIM_COLOR: "blue"},
        ]
    )
    product = Product(id=ObjectId(), name="Custom Bicycle", category="Bikes")

    order = Order(
        user_id=ObjectId(),
        order_items=[],
    )

    parts = [
        Part(
            name="full-suspension",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="road wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="blue",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]

    assert order.add_item(config, product, [], parts) == True
    order.fulfill()
    assert order.status == OrderStatus.FULFILLED
    assert order.order_items[0].product_id == product.id


def test_order_invalid_configuration_order_is_in_stock():
    rules = [
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

    invalid_config = Configuration(
        options=[
            {PartCategoryName.FRAME: "diamond"},
            {PartCategoryName.WHEELS: "mountain wheels"},
            {PartCategoryName.RIM_COLOR: "red"},
        ]
    )
    product = Product(
        id=ObjectId(),
        name="Custom Bicycle",
        category="Bikes",
        configuration_rule_ids=[rules[0].id, rules[1].id],
    )
    order = Order(
        user_id=ObjectId(),
        order_items=[],
    )

    parts = [
        Part(
            name="diamond",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="mountain wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="red",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]
    assert not order.add_item(invalid_config, product, rules, parts)


def test_order_valid_configuration_order_is_out_of_stock():
    config = Configuration(
        options=[
            {PartCategoryName.FRAME: "full-suspension"},
            {PartCategoryName.WHEELS: "road wheels"},
            {PartCategoryName.RIM_COLOR: "blue"},
        ]
    )

    product = Product(id=ObjectId(), name="Custom Bicycle", category="Bikes")

    order = Order(
        user_id=ObjectId(),
        order_items=[],
    )

    parts = [
        Part(
            name="full-suspension",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="road wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.OUT_OF_STOCK,
        ),
        Part(
            name="blue",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]

    assert order.add_item(config, product, [], parts) is False
