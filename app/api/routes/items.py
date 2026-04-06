from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate
from app.services import item_service

router = APIRouter(prefix="/items", tags=["items"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=ItemListResponse)
async def list_items(
    db: DbSession,
    skip: int = 0,
    limit: int = 100,
) -> ItemListResponse:
    items, total = await item_service.get_items(db, skip=skip, limit=limit)
    return ItemListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: DbSession) -> ItemResponse:
    return await item_service.get_item(db, item_id)


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(payload: ItemCreate, db: DbSession) -> ItemResponse:
    return await item_service.create_item(db, payload)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: DbSession,
) -> ItemResponse:
    return await item_service.update_item(db, item_id, payload)


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: DbSession) -> None:
    await item_service.delete_item(db, item_id)
