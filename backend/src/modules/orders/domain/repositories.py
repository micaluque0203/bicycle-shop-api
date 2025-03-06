from abc import ABC

from core.domain.repositories import GenericRepository
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.aggregates import Order


class OrderRepository(GenericRepository[PydanticObjectId, Order], ABC):
    """Interface for Order repository"""
