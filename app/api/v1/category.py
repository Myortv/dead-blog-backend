from typing import List


from fastapi import APIRouter, Depends, HTTPException

from app.controllers import category as category_controller

from app.schemas.category import (
    CategoryInDB,
    CategoryCreate,
    CategoryUpdate,
)

from app.permissions import category as category_permissions
from app.utils.deps import identify_request


api = APIRouter()


@api.get('/get-all', response_model=List[CategoryInDB])
async def get_all_categories(
):
    if result := await category_controller.get_all():
        return result
    raise HTTPException(404)


@api.get('/', response_model=CategoryInDB)
async def get_category_by_id(
    category_id: int
):
    if result := await category_controller.get_by_id(category_id):
        return result
    raise HTTPException(404)


@api.post('/', response_model=CategoryInDB)
async def create(
    category_data: CategoryCreate,
    identity: dict = Depends(identify_request),
):
    if await category_permissions.is_admin(identity):
        if result := await category_controller.create(
            category_data
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


@api.put('/', response_model=CategoryInDB)
async def update(
    category_id: int,
    category_data: CategoryUpdate,
    identity: dict = Depends(identify_request),
):
    if await category_permissions.is_admin(identity):
        if result := await category_controller.update(
            category_id,
            category_data
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


@api.delete('/', response_model=CategoryInDB)
async def delete(
    category_id: int,
    identity: dict = Depends(identify_request),
):
    if await category_permissions.is_admin(identity):
        if result := await category_controller.delete(
            category_id
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)
