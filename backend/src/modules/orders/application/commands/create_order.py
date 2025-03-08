from typing import List

from core.application.commands import Command, CommandResult
from core.domain.value_objects import PydanticObjectId
from modules.orders.domain.aggregates import Order
from modules.orders.domain.events import OrderCreatedEvent
from modules.orders.domain.repositories import OrderRepository
from modules.orders.domain.value_objects import (Configuration, OrderItem,
                                                 OrderStatus)
from modules.products.domain.repositories import (ConfigurationRuleRepository,
                                                  ProductRepository)


class CreateOrderItemCommand(Command):
    product_id: PydanticObjectId
    configuration: List[dict]


class CreateOrderCommand(Command):
    user_id: PydanticObjectId
    order_items: List[CreateOrderItemCommand] = []
    status: str = OrderStatus.PENDING


async def create_order_command(
    command: CreateOrderCommand,
    repository: OrderRepository,
    product_repository: ProductRepository,
    configuration_rule_repository: ConfigurationRuleRepository,
) -> CommandResult:

    # 1 - Validate user exits # TODO: create iam bounded context
    # 2 - Validate product exists
    # 3 - Get product configuration rules
    # 4 - Validate configuration against rules
    # 5 - Create order if not exists -> upsert

    if not command.order_items:
        return CommandResult.failure("Order must have at least one item")

    for item in command.order_items:
        product = await product_repository.get_by_id(item.product_id)
        if not product:
            return CommandResult.failure(f"Product {item.product_id} not found")

        if "configuration_rules_ids" in product:
            product_rules = await configuration_rule_repository.find_all_by_id(
                filter={"$in": product["configuration_rules_ids"]}
            )

            config = Configuration(options=item.configuration)

            if not config.is_valid(product_rules):
                return CommandResult.failure(
                    f"Invalid configuration for product {item.product_id}"
                )

    if user_order := await repository.get_by_user_id(command.user_id):
        # Check if the existing order is the same as the new order
        existing_order_items = user_order.order_items
        new_order_items = [
            OrderItem(
                product_id=item.product_id,
                configuration=item.configuration,
            )
            for item in command.order_items
        ]

        if existing_order_items == new_order_items:
            return CommandResult.success(
                entity_id=user_order.id,
                payload=user_order,
                event=None,
            )

        user_order.order_items = new_order_items
        order_created = await repository.update(user_order)
        if order_created:
            order_id = user_order.id
        else:
            raise Exception("Order not created")
    else:
        order = Order(
            user_id=command.user_id,
            order_items=[
                OrderItem(
                    product_id=item.product_id,
                    configuration=item.configuration,
                )
                for item in command.order_items
            ],
            status=command.status,
        )
        order_id = await repository.add(order)

    order_created = await repository.get_by_id(order_id)

    return CommandResult.success(
        entity_id=order_id,
        payload=order_created,
        event=OrderCreatedEvent(order_id=order_id),
    )
