from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.update_item_schema import UpdateItemCreate, UpdateItemRead, UpdateItemUpdate
from src.services.update_item_service import (
    create_update_item,
    list_update_items_by_update,
    list_update_items_by_item,
    update_update_item,
    delete_update_item,
    get_update_item,
    UpdateNotFoundError,
    ItemNotFoundError,
    UpdateItemNotFoundError,
    UpdateItemAlreadyExistsError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/update-items", tags=["update_items"])


@router.post("", response_model=UpdateItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: UpdateItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_update_item(session, payload)
    except (UpdateNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UpdateItemAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/by-update/{update_id}", response_model=list[UpdateItemRead])
@is_granted(RoleEnum.ADMIN)
def list_by_update(update_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # optionnel: tu peux lever 404 si update inexistante, mais liste vide est souvent OK
    return list_update_items_by_update(session, update_id)


@router.get("/by-item/{item_id}", response_model=list[UpdateItemRead])
@is_granted(RoleEnum.ADMIN)
def list_by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_update_items_by_item(session, item_id)


@router.get("", response_model=UpdateItemRead)
@is_granted(RoleEnum.ADMIN)
def get_one(update_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_update_item(session, update_id, item_id)
    except UpdateItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("", response_model=UpdateItemRead)
@is_granted(RoleEnum.ADMIN)
def patch(update_id: int, item_id: int, payload: UpdateItemUpdate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return update_update_item(session, update_id, item_id, payload)
    except UpdateItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete(update_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_update_item(session, update_id, item_id)
    except UpdateItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
