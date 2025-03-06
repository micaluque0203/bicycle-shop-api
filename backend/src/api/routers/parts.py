from typing import List

from fastapi import APIRouter, Depends

from api.dependencies.auth import current_superuser
from api.infrastructure.client import get_parts_repository
from core.domain.value_objects import PydanticObjectId
from modules.products.application.command.create_part import (
    CreatePartCommand, create_part_command)
from modules.products.application.command.delete_part import (
    DeletePartCommand, delete_part_command)
from modules.products.application.query.get_parts_listing import (
    GetPartListing, get_part_listing)
from modules.products.domain.entities import Part

router = APIRouter()


@router.post(
    "/admin/parts", response_model=Part, dependencies=[Depends(current_superuser)]
)
async def create_part(
    part: CreatePartCommand, repository=Depends(get_parts_repository)
):
    product_created = await create_part_command(part, repository)
    return Part(id=product_created.entity_id, **part.model_dump())


@router.get(
    "/admin/parts", response_model=List[Part], dependencies=[Depends(current_superuser)]
)  # TODO: add Response Model
async def get_parts(repository=Depends(get_parts_repository)):
    products = await get_part_listing(GetPartListing(), repository)
    if not products.payload:
        return []
    return products.payload


@router.delete(
    "/admin/parts/{part_id}",
    response_model=None,
    status_code=204,
    dependencies=[Depends(current_superuser)],
)
async def delete_part(
    part_id: PydanticObjectId, repository=Depends(get_parts_repository)
):
    await delete_part_command(DeletePartCommand(part_id=part_id), repository)


# @router.put(
#     "/admin/parts/{part_id}",
#     response_model=Part,
#     dependencies=[Depends(current_superuser)],
# )
# async def update_part(part_id: str, part: Part):
#     modified_count = repo.update_part(part_id, part.model_dump())
#     if modified_count == 0:
#         raise HTTPException(status_code=404, detail="Part not found")
#     return {"updated": True}


# @router.put(
#     "/admin/products/{product_id}/parts",
#     response_model=Product,
#     dependencies=[Depends(current_superuser)],
# )
# async def update_product_parts(product_id: str, part_ids: List[str]):
#     modified_count = repo.update_product_parts(product_id, part_ids)
#     if modified_count == 0:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return {"updated": True}
