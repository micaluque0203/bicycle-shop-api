from typing import List

from core.domain.entities import Aggregate
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.value_objects import (Configuration, OrderItem,
                                                 OrderStatus)
from modules.products.domain.aggregates import Product
from modules.products.domain.entities import ConfigurationRule


class Order(Aggregate):
    user_id: PydanticObjectId
    order_items: List[OrderItem] = []
    status: str = OrderStatus.PENDING

    def add_item(
        self,
        configuration: Configuration,
        product: Product,
        rules: List[ConfigurationRule],
    ) -> bool:
        if product.is_configuration_allowed(configuration, rules):
            self.order_items.append(configuration)
            return True
        return False

    def cancel(self):
        self.status = OrderStatus.CANCELLED

    def fulfill(self):
        self.status = OrderStatus.FULFILLED
