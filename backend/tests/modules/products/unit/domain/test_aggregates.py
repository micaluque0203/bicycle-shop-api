from src.modules.products.domain.aggregates import Configuration
from src.modules.products.domain.entities import ConfigurationRule
from src.modules.products.domain.value_objects import PartCategoryName


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
