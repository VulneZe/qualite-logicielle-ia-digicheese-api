from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.shop_schema import ShopCreate, ShopRead, ShopUpdate
from src.services.shop_service import (
    create_shop,
    list_shops,
    get_shop,
    list_shops_by_item,
    update_shop,
    delete_shop,
    ShopNotFoundError,
    ItemNotFoundError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("", response_model=ShopRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ShopCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_shop(session, payload)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[ShopRead])
@is_granted(RoleEnum.ADMIN)
def list_all(skip: int = 0, limit: int = 50, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_shops(session, skip=skip, limit=limit)


@router.get("/{shop_id}", response_model=ShopRead)
@is_granted(RoleEnum.ADMIN)
def get_one(shop_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_shop(session, shop_id)
    except ShopNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/by-item/{item_id}", response_model=list[ShopRead])
@is_granted(RoleEnum.ADMIN)
def list_by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_shops_by_item(session, item_id)


@router.patch("/{shop_id}", response_model=ShopRead)
@is_granted(RoleEnum.ADMIN)
def patch(shop_id: int, payload: ShopUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_shop(session, shop_id, payload)
    except ShopNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete(shop_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_shop(session, shop_id)
    except ShopNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
