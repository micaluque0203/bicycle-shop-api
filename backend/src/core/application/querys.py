from abc import ABC
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Query(BaseModel, ABC):
    """Abstract base class for all queries"""


class QueryResult(BaseModel, Generic[T]):
    payload: Optional[T] = None
    errors: list[Any] = Field(default_factory=list)

    @classmethod
    def success(cls, payload=None) -> "QueryResult":
        return cls(payload=payload)
