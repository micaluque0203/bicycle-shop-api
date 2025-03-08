from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.auth import current_superuser
from api.infrastructure.client import (get_parts_repository,
                                       get_products_repository,
                                       get_rules_repository)
from api.schemas.products import (ProductCreatedResponse, ProductResponse,
                                  UpdateProductRequest)
from core.domain.value_objects import PydanticObjectId
from modules.products.application.command.create_product import (
    CreateProductCommand, create_product_command)
from modules.products.application.command.delete_product import (
    DeleteProductCommand, delete_product_command)
from modules.products.application.command.update_product import (
    UpdateProductCommand, update_product_command)
from modules.products.application.query.get_product_details import (
    GetProductDetails, get_product_details)
from modules.products.application.query.get_products_listing import (
    GetProductListing, get_product_listing)

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    product_repository=Depends(get_products_repository),
    parts_repository=Depends(get_parts_repository),
    rules_repository=Depends(get_rules_repository),
):
    products = await get_product_listing(
        GetProductListing(),
        product_repository,
        parts_repository,
        rules_repository,
    )
    if not products.payload:
        return []

    return products.payload


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: PydanticObjectId,
    product_repository=Depends(get_products_repository),
    parts_repository=Depends(get_parts_repository),
    rules_repository=Depends(get_rules_repository),
):
    result = await get_product_details(
        GetProductDetails(product_id=product_id),
        product_repository,
        parts_repository,
        rules_repository,
    )
    if not result.payload:
        raise HTTPException(status_code=404, detail="Product not found")
    return result.payload


@router.post(
    "/admin/products",
    response_model=ProductCreatedResponse,
    status_code=201,
    # dependencies=[Depends(current_superuser)],
)
async def create_product(
    product: CreateProductCommand,
    repository=Depends(get_products_repository),
):
    product_created = await create_product_command(product, repository)
    return ProductCreatedResponse(product_id=product_created.entity_id)


@router.delete(
    "/admin/products/{product_id}",
    response_model=None,
    status_code=204,
    # dependencies=[Depends(current_superuser)],
)
async def delete_product(
    product_id: PydanticObjectId, repository=Depends(get_products_repository)
):
    await delete_product_command(
        DeleteProductCommand(product_id=product_id), repository
    )


@router.put(
    "/admin/products/{product_id}",
    status_code=200,
    # dependencies=[Depends(current_superuser)],
)
async def update_product(
    product_id: PydanticObjectId,
    product: UpdateProductRequest,
    repository=Depends(get_products_repository),
):
    product = UpdateProductCommand(
        product_id=product_id,
        name=product.name,
        category=product.category,
        part_ids=product.part_ids,
        configuration_rule_ids=product.configuration_rule_ids,
    )
    result = await update_product_command(product, repository)
    if result.has_errors():
        raise HTTPException(status_code=404, detail=result.error)

    if result.is_success() and result.events:
        return result.entity_id
