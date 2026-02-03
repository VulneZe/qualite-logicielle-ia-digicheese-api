from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.update import Update
from src.schemas.update_schema import UpdateCreate, UpdateUpdate


class UpdateNotFoundError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def create_update(session: Session, payload: UpdateCreate) -> Update:
    upd = Update(**_dump(payload))
    session.add(upd)
    session.commit()
    session.refresh(upd)
    return upd


def list_updates(session: Session, *, skip: int = 0, limit: int = 50) -> list[Update]:
    stmt = select(Update).order_by(Update.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_update(session: Session, update_id: int) -> Update:
    upd = session.get(Update, update_id)
    if not upd:
        raise UpdateNotFoundError(f"Update id={update_id} not found.")
    return upd


def update_update(session: Session, update_id: int, patch: UpdateUpdate) -> Update:
    upd = get_update(session, update_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(upd, key, value)

    session.add(upd)
    session.commit()
    session.refresh(upd)
    return upd


def delete_update(session: Session, update_id: int) -> None:
    upd = get_update(session, update_id)
    session.delete(upd)
    session.commit()