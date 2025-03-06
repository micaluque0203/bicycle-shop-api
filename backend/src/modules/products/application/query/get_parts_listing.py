from typing import List

from core.application.querys import Query, QueryResult
from modules.products.domain.repositories import PartRepository


class GetPartListing(Query):
    pass


async def get_part_listing(
    query: GetPartListing,
    repository: PartRepository,
) -> QueryResult:
    dao = await repository.get_all()
    return QueryResult.success(payload=dao)
