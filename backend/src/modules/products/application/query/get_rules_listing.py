from core.application.querys import Query, QueryResult
from modules.products.domain.repositories import ConfigurationRuleRepository


class GetRulesListing(Query):
    pass


async def get_configuration_rules_listing(
    query: GetRulesListing,
    repository: ConfigurationRuleRepository,
) -> QueryResult:
    dao = await repository.get_all()
    return QueryResult.success(payload=dao)
