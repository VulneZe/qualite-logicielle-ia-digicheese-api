from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.item import Item
from src.models.shop import Shop
from src.schemas.shop_schema import ShopCreate, ShopUpdate


class ShopNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def create_shop(session: Session, payload: ShopCreate) -> Shop:
    if not session.get(Item, payload.item_id):
        raise ItemNotFoundError(f"Item id={payload.item_id} not found.")

    shop = Shop(**_dump(payload))
    session.add(shop)
    session.commit()
    session.refresh(shop)
    return shop


def list_shops(session: Session, *, skip: int = 0, limit: int = 50) -> list[Shop]:
    stmt = select(Shop).order_by(Shop.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_shop(session: Session, shop_id: int) -> Shop:
    shop = session.get(Shop, shop_id)
    if not shop:
        raise ShopNotFoundError(f"Shop id={shop_id} not found.")
    return shop


def list_shops_by_item(session: Session, item_id: int) -> list[Shop]:
    stmt = select(Shop).where(Shop.item_id == item_id).order_by(Shop.id)
    return list(session.exec(stmt))


def update_shop(session: Session, shop_id: int, patch: ShopUpdate) -> Shop:
    shop = get_shop(session, shop_id)

    data = _dump(patch, exclude_unset=True)

    if "item_id" in data:
        if not session.get(Item, data["item_id"]):
            raise ItemNotFoundError(f"Item id={data['item_id']} not found.")

    for key, value in data.items():
        setattr(shop, key, value)

    session.add(shop)
    session.commit()
    session.refresh(shop)
    return shop


def delete_shop(session: Session, shop_id: int) -> None:
    shop = get_shop(session, shop_id)
    session.delete(shop)
    session.commit()
