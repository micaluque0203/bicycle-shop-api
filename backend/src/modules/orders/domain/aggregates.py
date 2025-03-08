from typing import List

from core.domain.entities import Aggregate
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.value_objects import (Configuration, OrderItem,
                                                 OrderStatus)
from modules.products.domain.aggregates import Product
from modules.products.domain.entities import ConfigurationRule, Part


class Order(Aggregate):
    user_id: PydanticObjectId
    order_items: List[OrderItem] = []
    status: str = OrderStatus.PENDING

    def add_item(
        self,
        configuration: Configuration,
        product: Product,
        rules: List[ConfigurationRule],
        parts: List[Part],
    ) -> bool:

        if self.status == OrderStatus.PENDING:
            if product.is_configuration_allowed(
                configuration, rules
            ) and configuration.is_in_stock(parts):
                item = OrderItem(
                    product_id=product.id, configuration=configuration.options
                )
                self.order_items.append(item)
                return True
            return False

    def cancel(self):
        self.status = OrderStatus.CANCELLED

    def fulfill(self):
        self.status = OrderStatus.FULFILLED
