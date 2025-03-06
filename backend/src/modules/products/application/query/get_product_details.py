from core.application.querys import Query, QueryResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.repositories import (ConfigurationRuleRepository,
                                                  PartRepository,
                                                  ProductRepository)


class GetProductDetails(Query):
    product_id: PydanticObjectId


async def get_product_details(
    query: GetProductDetails,
    product_repository: ProductRepository,
    parts_repository: PartRepository,
    rules_repository: ConfigurationRuleRepository,
) -> QueryResult:
    product = await product_repository.get_by_id(query.product_id)

    print(product)

    if product is None:
        raise ValueError("Product not found")

    parts = await parts_repository.find_all_by_id(
        filter={"$in": product.get("part_ids", [])}
    )
    configuration_rules = await rules_repository.find_all_by_id(
        filter={"$in": product.get("configuration_rule_ids", [])}
    )

    product_detail = {
        "product_id": product["_id"],
        "category": product["category"],
        "name": product["name"],
        "available_parts": parts,
        "configuration_rules": configuration_rules,
    }

    return QueryResult(payload=product_detail)
