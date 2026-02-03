# src/services/item_service.py
from __future__ import annotations

from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.models.item import Item
from src.schemas.item_schema import ItemCreate, ItemUpdate


# ----------------------------
# Exceptions "métier"
# (le router les convertira en 404/409)
# ----------------------------
class ItemNotFoundError(Exception):
    pass


class ItemCodeAlreadyExistsError(Exception):
    pass


# ----------------------------
# Helper compat Pydantic v1/v2
# ----------------------------
def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    """
    Pydantic v2 -> model_dump()
    Pydantic v1 -> dict()
    """
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


# ----------------------------
# CRUD
# ----------------------------
def create_item(session: Session, payload: ItemCreate) -> Item:
    """
    Crée un item.
    - code est unique (contrainte DB), on renvoie une erreur métier si doublon
    """
    item = Item(**_dump(payload))
    session.add(item)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ItemCodeAlreadyExistsError("An item with this code already exists.") from e

    session.refresh(item)
    return item


def list_items(session: Session, *, skip: int = 0, limit: int = 50) -> list[Item]:
    """
    Liste paginée simple.
    (Si tu veux de la recherche/filtres, on ajoutera un ItemSearch ensuite.)
    """
    stmt = select(Item).order_by(Item.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_item(session: Session, item_id: int) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise ItemNotFoundError(f"Item id={item_id} not found.")
    return item


def get_item_by_code(session: Session, code: int) -> Item:
    stmt = select(Item).where(Item.code == code)
    item = session.exec(stmt).first()
    if not item:
        raise ItemNotFoundError(f"Item code={code} not found.")
    return item


def update_item(session: Session, item_id: int, patch: ItemUpdate) -> Item:
    """
    PATCH : applique uniquement les champs fournis.
    Gère aussi le cas où on change code -> doublon => erreur métier
    """
    item = get_item(session, item_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(item, key, value)

    session.add(item)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ItemCodeAlreadyExistsError("An item with this code already exists.") from e

    session.refresh(item)
    return item


def delete_item(session: Session, item_id: int) -> None:
    """
    DELETE standard : suppression puis commit.
    (Le router peut répondre 204 No Content.)
    """
    item = get_item(session, item_id)
    session.delete(item)
    session.commit()