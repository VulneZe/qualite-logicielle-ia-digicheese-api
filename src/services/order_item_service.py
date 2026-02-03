from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.commande import Commande
from src.models.item import Item
from src.models.link.order_item_link import OrderItemLink
from src.schemas.order_item_schema import OrderItemCreate, OrderItemUpdate


class CommandeNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class OrderItemNotFoundError(Exception):
    pass


class OrderItemAlreadyExistsError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def _ensure_commande_exists(session: Session, commande_id: int) -> None:
    if not session.get(Commande, commande_id):
        raise CommandeNotFoundError(f"Commande id={commande_id} not found.")


def _ensure_item_exists(session: Session, item_id: int) -> None:
    if not session.get(Item, item_id):
        raise ItemNotFoundError(f"Item id={item_id} not found.")


def get_order_item(session: Session, commande_id: int, item_id: int) -> OrderItemLink:
    link = session.get(OrderItemLink, (commande_id, item_id))
    if not link:
        raise OrderItemNotFoundError(
            f"OrderItem (commande_id={commande_id}, item_id={item_id}) not found."
        )
    return link


def list_order_items_by_commande(session: Session, commande_id: int) -> list[OrderItemLink]:
    stmt = (
        select(OrderItemLink)
        .where(OrderItemLink.commande_id == commande_id)
        .order_by(OrderItemLink.item_id)
    )
    return list(session.exec(stmt))


def list_order_items_by_item(session: Session, item_id: int) -> list[OrderItemLink]:
    stmt = (
        select(OrderItemLink)
        .where(OrderItemLink.item_id == item_id)
        .order_by(OrderItemLink.commande_id)
    )
    return list(session.exec(stmt))


def create_order_item(session: Session, payload: OrderItemCreate) -> OrderItemLink:
    _ensure_commande_exists(session, payload.commande_id)
    _ensure_item_exists(session, payload.item_id)

    existing = session.get(OrderItemLink, (payload.commande_id, payload.item_id))
    if existing:
        raise OrderItemAlreadyExistsError(
            f"OrderItem already exists (commande_id={payload.commande_id}, item_id={payload.item_id})."
        )

    link = OrderItemLink(**_dump(payload))
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def update_order_item(
    session: Session,
    commande_id: int,
    item_id: int,
    patch: OrderItemUpdate,
) -> OrderItemLink:
    link = get_order_item(session, commande_id, item_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(link, key, value)

    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def delete_order_item(session: Session, commande_id: int, item_id: int) -> None:
    link = get_order_item(session, commande_id, item_id)
    session.delete(link)
    session.commit()