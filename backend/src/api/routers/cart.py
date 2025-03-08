from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.auth import current_active_user
from api.infrastructure.client import (
    get_orders_repository,
    get_parts_repository,
    get_products_repository,
    get_rules_repository,
)
from api.schemas.orders import ValidateOrderItemRequest, ValidateOrderItemResponse
from core.domain.value_objects import PydanticObjectId
from modules.orders.application.commands.create_order import (
    CreateOrderCommand,
    CreateOrderItemCommand,
    create_order_command,
)
from modules.orders.application.commands.validate_order_item import (
    ValidateOrderItemCommand,
    validate_order_item_command,
)
from modules.orders.domain.aggregates import Order
from modules.orders.domain.value_objects import Configuration

router = APIRouter()


@router.post("/cart", response_model=Order)
async def add_to_cart(
    configuration: Configuration,
    product_id: PydanticObjectId,
    user=Depends(current_active_user),
    repository=Depends(get_orders_repository),
    rules_repository=Depends(get_rules_repository),
    product_repository=Depends(get_products_repository),
):

    order_command = CreateOrderCommand(
        user_id=user.id,
        order_items=[
            CreateOrderItemCommand(
                product_id=product_id, configuration=configuration.options
            )
        ],
    )

    order_created = await create_order_command(
        order_command, repository, product_repository, rules_repository
    )
    return Order(id=order_created.entity_id, **order_created.payload)


@router.post("/validate-order-item", response_model=ValidateOrderItemResponse)
async def validate_order_item(
    request: ValidateOrderItemRequest,
    product_repository=Depends(get_products_repository),
    parts_repository=Depends(get_parts_repository),
    rules_repository=Depends(get_rules_repository),
):
    response = await validate_order_item_command(
        ValidateOrderItemCommand(
            product_id=request.product_id, configuration=request.configuration
        ),
        product_repository,
        parts_repository,
        rules_repository,
    )

    if response.has_errors():
        raise HTTPException(status_code=400, detail=response.errors[0][0])

    return ValidateOrderItemResponse(is_valid=True)
