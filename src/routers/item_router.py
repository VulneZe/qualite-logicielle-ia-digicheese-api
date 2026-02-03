from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.item_schema import ItemCreate, ItemRead, ItemUpdate
from src.services.item_service import (
    create_item,
    list_items,
    get_item,
    update_item,
    delete_item,
    ItemNotFoundError,
    ItemCodeAlreadyExistsError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_item(session, payload)
    except ItemCodeAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[ItemRead])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def list_all(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 50,
    current_user=Depends(get_current_user),
):
    return list_items(session, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def get_one(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_item(session, item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{item_id}", response_model=ItemRead)
@is_granted(RoleEnum.ADMIN)
def patch_one(item_id: int, patch: ItemUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_item(session, item_id, patch)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ItemCodeAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_one(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_item(session, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
