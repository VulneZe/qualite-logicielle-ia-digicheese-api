from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.item import Item
from src.models.update import Update
from src.models.link.update_item_link import UpdateItemLink
from src.schemas.update_item_schema import UpdateItemCreate, UpdateItemUpdate


class UpdateNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class UpdateItemNotFoundError(Exception):
    pass


class UpdateItemAlreadyExistsError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def _ensure_update_exists(session: Session, update_id: int) -> None:
    if not session.get(Update, update_id):
        raise UpdateNotFoundError(f"Update id={update_id} not found.")


def _ensure_item_exists(session: Session, item_id: int) -> None:
    if not session.get(Item, item_id):
        raise ItemNotFoundError(f"Item id={item_id} not found.")


def get_update_item(session: Session, update_id: int, item_id: int) -> UpdateItemLink:
    link = session.get(UpdateItemLink, (update_id, item_id))
    if not link:
        raise UpdateItemNotFoundError(f"UpdateItem (update_id={update_id}, item_id={item_id}) not found.")
    return link


def list_update_items_by_update(session: Session, update_id: int) -> list[UpdateItemLink]:
    stmt = (
        select(UpdateItemLink)
        .where(UpdateItemLink.update_id == update_id)
        .order_by(UpdateItemLink.item_id)
    )
    return list(session.exec(stmt))


def list_update_items_by_item(session: Session, item_id: int) -> list[UpdateItemLink]:
    stmt = (
        select(UpdateItemLink)
        .where(UpdateItemLink.item_id == item_id)
        .order_by(UpdateItemLink.update_id)
    )
    return list(session.exec(stmt))


def create_update_item(session: Session, payload: UpdateItemCreate) -> UpdateItemLink:
    _ensure_update_exists(session, payload.update_id)
    _ensure_item_exists(session, payload.item_id)

    existing = session.get(UpdateItemLink, (payload.update_id, payload.item_id))
    if existing:
        raise UpdateItemAlreadyExistsError(
            f"UpdateItem already exists (update_id={payload.update_id}, item_id={payload.item_id})."
        )

    link = UpdateItemLink(**_dump(payload))
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def update_update_item(
    session: Session,
    update_id: int,
    item_id: int,
    patch: UpdateItemUpdate,
) -> UpdateItemLink:
    link = get_update_item(session, update_id, item_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(link, key, value)

    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def delete_update_item(session: Session, update_id: int, item_id: int) -> None:
    link = get_update_item(session, update_id, item_id)
    session.delete(link)
    session.commit()