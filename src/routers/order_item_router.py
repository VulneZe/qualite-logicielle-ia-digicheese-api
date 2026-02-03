from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.order_item_schema import OrderItemCreate, OrderItemRead, OrderItemUpdate
from src.services.order_item_service import (
    create_order_item,
    list_order_items_by_commande,
    list_order_items_by_item,
    update_order_item,
    delete_order_item,
    get_order_item,
    CommandeNotFoundError,
    ItemNotFoundError,
    OrderItemNotFoundError,
    OrderItemAlreadyExistsError,
)

# ajouts sécurité ADMIN + OP_COLIS
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/order-items", tags=["order_items"])


@router.post("", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def create(payload: OrderItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_order_item(session, payload)
    except (CommandeNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OrderItemAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/by-commande/{commande_id}", response_model=list[OrderItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def list_by_commande(commande_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_order_items_by_commande(session, commande_id)


@router.get("/by-item/{item_id}", response_model=list[OrderItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def list_by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_order_items_by_item(session, item_id)


@router.get("", response_model=OrderItemRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def get_one(commande_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_order_item(session, commande_id, item_id)
    except OrderItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("", response_model=OrderItemRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def patch(commande_id: int, item_id: int, payload: OrderItemUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_order_item(session, commande_id, item_id, payload)
    except OrderItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def delete(commande_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_order_item(session, commande_id, item_id)
    except OrderItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
