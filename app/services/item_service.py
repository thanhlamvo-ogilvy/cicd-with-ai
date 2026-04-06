from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> tuple[list[Item], int]:
    count_result = await db.execute(select(func.count()).select_from(Item))
    total = count_result.scalar_one()

    result = await db.execute(select(Item).offset(skip).limit(limit))
    items = list(result.scalars().all())
    return items, total


async def get_item(db: AsyncSession, item_id: int) -> Item:
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


async def create_item(db: AsyncSession, payload: ItemCreate) -> Item:
    item = Item(**payload.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


async def update_item(db: AsyncSession, item_id: int, payload: ItemUpdate) -> Item:
    item = await get_item(db, item_id)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    await db.flush()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item_id: int) -> None:
    item = await get_item(db, item_id)
    await db.delete(item)
    await db.flush()
