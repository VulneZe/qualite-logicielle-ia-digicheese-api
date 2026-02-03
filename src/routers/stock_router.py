from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.stock_schema import StockCreate, StockRead, StockUpdate
from src.services.stock_service import (
    create_stock,
    list_stocks,
    get_stock,
    update_stock,
    delete_stock,
    StockNotFoundError,
)

# ajouts sécurité ADMIN + OP_STOCK
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.post("", response_model=StockRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def create(payload: StockCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return create_stock(session, payload)


@router.get("", response_model=list[StockRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def list_all(skip: int = 0, limit: int = 50, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_stocks(session, skip=skip, limit=limit)


@router.get("/{stock_id}", response_model=StockRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def get_one(stock_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_stock(session, stock_id)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{stock_id}", response_model=StockRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def patch(stock_id: int, payload: StockUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_stock(session, stock_id, payload)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_STOCK)
def delete(stock_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_stock(session, stock_id)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
