from typing import List

from core.application.querys import Query, QueryResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.aggregates import Product
from modules.products.domain.repositories import (
    ConfigurationRuleRepository,
    PartRepository,
    ProductRepository,
)


class GetProductListing(Query):
    pass


async def get_product_listing(
    query: GetProductListing,
    product_repository: ProductRepository,
    parts_repository: PartRepository,
    rules_repository: ConfigurationRuleRepository,
) -> QueryResult:

    products = await product_repository.get_all()

    product_listings = []

    for product in products:
        parts = await parts_repository.find_all_by_id({"$in": product.part_ids})

        configuration_rules = await rules_repository.find_all_by_id(
            {"$in": product.configuration_rule_ids}
        )
        product_listing = {
            "product_id": product.id,
            "category": product.category,
            "name": product.name,
            "available_parts": [part.model_dump() for part in parts],
            "configuration_rules": [rule.model_dump() for rule in configuration_rules],
        }
        product_listings.append(product_listing)

    return QueryResult.success(payload=product_listings)
