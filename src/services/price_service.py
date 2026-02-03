from __future__ import annotations

from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.models.price import Price
from src.models.item import Item
from src.schemas.price_schema import PriceCreate, PriceUpdate


class PriceNotFoundError(Exception):
    pass


class PriceAlreadyExistsForItemError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def create_price(session: Session, payload: PriceCreate) -> Price:
    # Vérifie que l'item existe (sinon FK error pas très lisible)
    item = session.get(Item, payload.item_id)
    if not item:
        raise ItemNotFoundError(f"Item id={payload.item_id} not found.")

    price = Price(**_dump(payload))
    session.add(price)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        # UNIQUE(item_id) -> 1 seul prix par item
        raise PriceAlreadyExistsForItemError(
            f"Price already exists for item_id={payload.item_id}."
        ) from e

    session.refresh(price)
    return price


def list_prices(session: Session, *, skip: int = 0, limit: int = 50) -> list[Price]:
    stmt = select(Price).order_by(Price.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_price(session: Session, price_id: int) -> Price:
    price = session.get(Price, price_id)
    if not price:
        raise PriceNotFoundError(f"Price id={price_id} not found.")
    return price


def get_price_by_item(session: Session, item_id: int) -> Price:
    stmt = select(Price).where(Price.item_id == item_id)
    price = session.exec(stmt).first()
    if not price:
        raise PriceNotFoundError(f"Price for item_id={item_id} not found.")
    return price


def update_price(session: Session, price_id: int, patch: PriceUpdate) -> Price:
    price = get_price(session, price_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(price, key, value)

    session.add(price)
    session.commit()
    session.refresh(price)
    return price


def delete_price(session: Session, price_id: int) -> None:
    price = get_price(session, price_id)
    session.delete(price)
    session.commit()