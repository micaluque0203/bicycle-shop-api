from abc import ABC

from core.domain.repositories import GenericRepository
from core.domain.value_objects import PydanticObjectId
from modules.products.domain.aggregates import Product
from modules.products.domain.entities import ConfigurationRule, Part


class ProductRepository(GenericRepository[PydanticObjectId, Product], ABC):
    """Interface for Product repository"""


class PartRepository(GenericRepository[PydanticObjectId, Part], ABC):
    """Interface for Part repository"""


class ConfigurationRuleRepository(
    GenericRepository[PydanticObjectId, ConfigurationRule], ABC
):
    """Interface for Configuration Rule repository"""
