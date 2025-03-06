from core.application.querys import Query, QueryResult
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.repositories import ConfigurationRuleRepository


class GetConfigurationRuleDetails(Query):
    rule_id: PydanticObjectId


async def get_rule_configuration_details(
    query: GetConfigurationRuleDetails,
    repository: ConfigurationRuleRepository,
) -> QueryResult:
    dao = await repository.get_by_id(query.rule_id)
    if dao is None:
        raise ValueError("Rule not found")
    return QueryResult(payload=dao)
