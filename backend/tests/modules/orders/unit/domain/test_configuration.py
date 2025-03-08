from src.modules.orders.domain.value_objects import Configuration
from src.modules.products.domain.aggregates import Configuration
from src.modules.products.domain.entities import ConfigurationRule, Part
from src.modules.products.domain.value_objects import PartCategoryName, StockStatus


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


def test_configuration_parts_in_stock():
    parts = [
        Part(
            name="Full-suspension",
            part_type=PartCategoryName.FRAME,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="Matte",
            part_type=PartCategoryName.FRAME_FINISH,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="Road wheels",
            part_type=PartCategoryName.WHEELS,
            stock_status=StockStatus.AVAILABLE,
        ),
        Part(
            name="Red",
            part_type=PartCategoryName.RIM_COLOR,
            stock_status=StockStatus.OUT_OF_STOCK,
        ),
        Part(
            name="Single-speed chain",
            part_type=PartCategoryName.CHAIN,
            stock_status=StockStatus.AVAILABLE,
        ),
    ]

    configuration = Configuration(
        options=[
            {PartCategoryName.FRAME: "Full-suspension"},
            {PartCategoryName.FRAME_FINISH: "Matte"},
            {PartCategoryName.WHEELS: "Road wheels"},
            {PartCategoryName.RIM_COLOR: "Red"},
            {PartCategoryName.CHAIN: "Single-speed chain"},
        ]
    )

    assert configuration.is_in_stock(parts) is False

    parts[3].stock_status = StockStatus.AVAILABLE
    assert configuration.is_in_stock(parts)
