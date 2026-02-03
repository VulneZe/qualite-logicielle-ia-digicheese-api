from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.conditionnement import Conditionnement
from src.models.item import Item
from src.models.link.conditionnement_item_link import ConditionnementItemLink
from src.schemas.conditionnement_item_schema import (
    ConditionnementItemCreate,
    ConditionnementItemUpdate,
)


# ---------- Errors (pour router -> HTTP codes) ----------
class ConditionnementNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class ConditionnementItemNotFoundError(Exception):
    pass


class ConditionnementItemAlreadyExistsError(Exception):
    pass


class QuantityRangeError(Exception):
    pass


# ---------- Utils ----------
def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def _ensure_conditionnement_exists(session: Session, conditionnement_id: int) -> None:
    if not session.get(Conditionnement, conditionnement_id):
        raise ConditionnementNotFoundError(f"Conditionnement id={conditionnement_id} not found.")


def _ensure_item_exists(session: Session, item_id: int) -> None:
    if not session.get(Item, item_id):
        raise ItemNotFoundError(f"Item id={item_id} not found.")


def _validate_qty_range(quantity_min: int, quantity_max: int) -> None:
    if quantity_min > quantity_max:
        raise QuantityRangeError("quantity_min must be <= quantity_max.")


# ---------- CRUD ----------
def get_link(session: Session, conditionnement_id: int, item_id: int) -> ConditionnementItemLink:
    link = session.get(ConditionnementItemLink, (conditionnement_id, item_id))
    if not link:
        raise ConditionnementItemNotFoundError(
            f"ConditionnementItemLink (conditionnement_id={conditionnement_id}, item_id={item_id}) not found."
        )
    return link


def list_by_conditionnement(session: Session, conditionnement_id: int) -> list[ConditionnementItemLink]:
    stmt = (
        select(ConditionnementItemLink)
        .where(ConditionnementItemLink.conditionnement_id == conditionnement_id)
        .order_by(ConditionnementItemLink.item_id)
    )
    return list(session.exec(stmt))


def list_by_item(session: Session, item_id: int) -> list[ConditionnementItemLink]:
    stmt = (
        select(ConditionnementItemLink)
        .where(ConditionnementItemLink.item_id == item_id)
        .order_by(ConditionnementItemLink.conditionnement_id)
    )
    return list(session.exec(stmt))


def create_link(session: Session, payload: ConditionnementItemCreate) -> ConditionnementItemLink:
    _ensure_conditionnement_exists(session, payload.conditionnement_id)
    _ensure_item_exists(session, payload.item_id)
    _validate_qty_range(payload.quantity_min, payload.quantity_max)

    existing = session.get(ConditionnementItemLink, (payload.conditionnement_id, payload.item_id))
    if existing:
        raise ConditionnementItemAlreadyExistsError(
            f"Link already exists (conditionnement_id={payload.conditionnement_id}, item_id={payload.item_id})."
        )

    link = ConditionnementItemLink(**_dump(payload))
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def update_link(
    session: Session,
    conditionnement_id: int,
    item_id: int,
    patch: ConditionnementItemUpdate,
) -> ConditionnementItemLink:
    link = get_link(session, conditionnement_id, item_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(link, key, value)

    # re-valider après patch
    _validate_qty_range(link.quantity_min, link.quantity_max)

    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def delete_link(session: Session, conditionnement_id: int, item_id: int) -> None:
    link = get_link(session, conditionnement_id, item_id)
    session.delete(link)
    session.commit()
