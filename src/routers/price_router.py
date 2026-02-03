from __future__ import annotations
from src.config.database import get_session

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.schemas.price_schema import PriceCreate, PriceRead, PriceUpdate

from src.services.price_service import (
    create_price,
    list_prices,
    get_price,
    update_price,
    delete_price,
    get_price_by_item,
    PriceNotFoundError,
    PriceAlreadyExistsForItemError,
    ItemNotFoundError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/prices", tags=["prices"])


@router.post("", response_model=PriceRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: PriceCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_price(session, payload)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PriceAlreadyExistsForItemError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[PriceRead])
@is_granted(RoleEnum.ADMIN)
def list_all(skip: int = 0, limit: int = 50, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_prices(session, skip=skip, limit=limit)


@router.get("/{price_id}", response_model=PriceRead)
@is_granted(RoleEnum.ADMIN)
def get_one(price_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_price(session, price_id)
    except PriceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by-item/{item_id}", response_model=PriceRead)
@is_granted(RoleEnum.ADMIN)
def get_one_by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_price_by_item(session, item_id)
    except PriceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{price_id}", response_model=PriceRead)
@is_granted(RoleEnum.ADMIN)
def patch(price_id: int, payload: PriceUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_price(session, price_id, payload)
    except PriceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete(price_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_price(session, price_id)
    except PriceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
