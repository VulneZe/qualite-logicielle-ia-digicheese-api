from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.item import Item
from src.models.stock import Stock
from src.models.stock_line import StockLine
from src.schemas.stock_line_schema import StockLineCreate, StockLineUpdate


class StockLineNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class StockNotFoundError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def create_stock_line(session: Session, payload: StockLineCreate) -> StockLine:
    # Vérifie que l'item existe (sinon FK error pas très lisible)
    item = session.get(Item, payload.item_id)
    if not item:
        raise ItemNotFoundError(f"Item id={payload.item_id} not found.")

    # stock_id est optionnel
    if payload.stock_id is not None:
        stock = session.get(Stock, payload.stock_id)
        if not stock:
            raise StockNotFoundError(f"Stock id={payload.stock_id} not found.")

    stock_line = StockLine(**_dump(payload))
    session.add(stock_line)
    session.commit()
    session.refresh(stock_line)
    return stock_line


def list_stock_lines(session: Session, *, skip: int = 0, limit: int = 50) -> list[StockLine]:
    stmt = select(StockLine).order_by(StockLine.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_stock_line(session: Session, stock_line_id: int) -> StockLine:
    stock_line = session.get(StockLine, stock_line_id)
    if not stock_line:
        raise StockLineNotFoundError(f"StockLine id={stock_line_id} not found.")
    return stock_line


def get_stock_lines_by_item(session: Session, item_id: int) -> list[StockLine]:
    stmt = select(StockLine).where(StockLine.item_id == item_id).order_by(StockLine.id)
    return list(session.exec(stmt))


def update_stock_line(session: Session, stock_line_id: int, patch: StockLineUpdate) -> StockLine:
    stock_line = get_stock_line(session, stock_line_id)

    data = _dump(patch, exclude_unset=True)

    # Si on change item_id / stock_id, on vérifie l'existence
    if "item_id" in data:
        item = session.get(Item, data["item_id"])
        if not item:
            raise ItemNotFoundError(f"Item id={data['item_id']} not found.")

    if "stock_id" in data:
        if data["stock_id"] is not None:
            stock = session.get(Stock, data["stock_id"])
            if not stock:
                raise StockNotFoundError(f"Stock id={data['stock_id']} not found.")

    for key, value in data.items():
        setattr(stock_line, key, value)

    session.add(stock_line)
    session.commit()
    session.refresh(stock_line)
    return stock_line


def delete_stock_line(session: Session, stock_line_id: int) -> None:
    stock_line = get_stock_line(session, stock_line_id)
    session.delete(stock_line)
    session.commit()
