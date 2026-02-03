from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.stock_line_schema import StockLineCreate, StockLineRead, StockLineUpdate
from src.services.stock_line_service import (
    create_stock_line,
    list_stock_lines,
    get_stock_line,
    get_stock_lines_by_item,
    update_stock_line,
    delete_stock_line,
    StockLineNotFoundError,
    ItemNotFoundError,
    StockNotFoundError,
)

# ajouts sécurité ADMIN + OP_STOCK
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/stock-lines", tags=["stock_lines"])


@router.post("", response_model=StockLineRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def create(payload: StockLineCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_stock_line(session, payload)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[StockLineRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def list_all(skip: int = 0, limit: int = 50, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_stock_lines(session, skip=skip, limit=limit)


@router.get("/{stock_line_id}", response_model=StockLineRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def get_one(stock_line_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_stock_line(session, stock_line_id)
    except StockLineNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by-item/{item_id}", response_model=list[StockLineRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def list_by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return get_stock_lines_by_item(session, item_id)


@router.patch("/{stock_line_id}", response_model=StockLineRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def patch(stock_line_id: int, payload: StockLineUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_stock_line(session, stock_line_id, payload)
    except StockLineNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{stock_line_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def delete(stock_line_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_stock_line(session, stock_line_id)
    except StockLineNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
