from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.auth import current_superuser
from api.infrastructure.client import get_parts_repository
from api.schemas.parts import PartResponse
from core.domain.value_objects import PydanticObjectId
from modules.products.application.command.create_part import (
    CreatePartCommand, create_part_command)
from modules.products.application.command.delete_part import (
    DeletePartCommand, delete_part_command)
from modules.products.application.command.update_part import (
    UpdatePartCommand, update_part_command)
from modules.products.application.query.get_parts_listing import (
    GetPartListing, get_part_listing)

router = APIRouter()


@router.post(
    "/admin/parts",
    response_model=PartResponse,
    # dependencies=[Depends(current_superuser)],
)
async def create_part(
    part: CreatePartCommand, repository=Depends(get_parts_repository)
):
    product_created = await create_part_command(part, repository)
    return PartResponse(id=product_created.entity_id, **part.model_dump())


@router.get(
    "/admin/parts",
    response_model=List[PartResponse],
    # dependencies=[Depends(current_superuser)],
)
async def get_parts(repository=Depends(get_parts_repository)):
    products = await get_part_listing(GetPartListing(), repository)
    if not products.payload:
        return []
    return products.payload


@router.delete(
    "/admin/parts/{part_id}",
    response_model=None,
    status_code=204,
    # dependencies=[Depends(current_superuser)],
)
async def delete_part(
    part_id: PydanticObjectId, repository=Depends(get_parts_repository)
):
    await delete_part_command(DeletePartCommand(part_id=part_id), repository)


@router.put(
    "/admin/products/{product_id}",
    response_model=PartResponse,
    status_code=200,
    # dependencies=[Depends(current_superuser)],
)
async def update_part(
    part: UpdatePartCommand, repository=Depends(get_parts_repository)
):
    result = await update_part_command(part, repository)
    if result.has_errors:
        raise HTTPException(status_code=404, detail=result.error)

    if result.is_success and result.events:
        return result.events[0].model_dump()
