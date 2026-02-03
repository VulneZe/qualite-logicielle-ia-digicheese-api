from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.update_schema import UpdateCreate, UpdateRead, UpdateUpdate
from src.services.update_service import (
    create_update,
    list_updates,
    get_update,
    update_update,
    delete_update,
    UpdateNotFoundError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/updates", tags=["updates"])


@router.post("", response_model=UpdateRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(
    payload: UpdateCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return create_update(session, payload)


@router.get("", response_model=list[UpdateRead])
@is_granted(RoleEnum.ADMIN)
def list_all(
    skip: int = 0,
    limit: int = 50,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return list_updates(session, skip=skip, limit=limit)


@router.get("/{update_id}", response_model=UpdateRead)
@is_granted(RoleEnum.ADMIN)
def get_one(
    update_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        return get_update(session, update_id)
    except UpdateNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{update_id}", response_model=UpdateRead)
@is_granted(RoleEnum.ADMIN)
def patch(
    update_id: int,
    payload: UpdateUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        return update_update(session, update_id, payload)
    except UpdateNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{update_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete(
    update_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        delete_update(session, update_id)
    except UpdateNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
