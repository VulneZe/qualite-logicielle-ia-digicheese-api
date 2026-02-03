from __future__ import annotations

from typing import Any

from sqlmodel import Session, select

from src.models.stock import Stock
from src.schemas.stock_schema import StockCreate, StockUpdate


class StockNotFoundError(Exception):
    pass


def _dump(obj: Any, *, exclude_unset: bool = False) -> dict:
    # compat pydantic v1/v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_unset=exclude_unset)
    return obj.dict(exclude_unset=exclude_unset)


def create_stock(session: Session, payload: StockCreate) -> Stock:
    stock = Stock(**_dump(payload))
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


def list_stocks(session: Session, *, skip: int = 0, limit: int = 50) -> list[Stock]:
    stmt = select(Stock).order_by(Stock.id).offset(skip).limit(limit)
    return list(session.exec(stmt))


def get_stock(session: Session, stock_id: int) -> Stock:
    stock = session.get(Stock, stock_id)
    if not stock:
        raise StockNotFoundError(f"Stock id={stock_id} not found.")
    return stock


def update_stock(session: Session, stock_id: int, patch: StockUpdate) -> Stock:
    stock = get_stock(session, stock_id)

    data = _dump(patch, exclude_unset=True)
    for key, value in data.items():
        setattr(stock, key, value)

    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


def delete_stock(session: Session, stock_id: int) -> None:
    stock = get_stock(session, stock_id)
    session.delete(stock)
    session.commit()
