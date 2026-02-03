from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.config.database import get_session
from src.schemas.conditionnement_item_schema import (
    ConditionnementItemCreate,
    ConditionnementItemRead,
    ConditionnementItemUpdate,
)
from src.services.conditionnement_item_service import (
    create_link,
    delete_link,
    get_link,
    list_by_conditionnement,
    list_by_item,
    update_link,
    ConditionnementNotFoundError,
    ItemNotFoundError,
    ConditionnementItemNotFoundError,
    ConditionnementItemAlreadyExistsError,
    QuantityRangeError,
)

# ajouts sécurité ADMIN only
from src import RoleEnum
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter(prefix="/conditionnement-items", tags=["conditionnement_items"])


@router.post("", response_model=ConditionnementItemRead, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create(payload: ConditionnementItemCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return create_link(session, payload)
    except (ConditionnementNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConditionnementItemAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except QuantityRangeError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/by-conditionnement/{conditionnement_id}", response_model=list[ConditionnementItemRead])
@is_granted(RoleEnum.ADMIN)
def by_conditionnement(conditionnement_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_by_conditionnement(session, conditionnement_id)


@router.get("/by-item/{item_id}", response_model=list[ConditionnementItemRead])
@is_granted(RoleEnum.ADMIN)
def by_item(item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return list_by_item(session, item_id)


@router.get("", response_model=ConditionnementItemRead)
@is_granted(RoleEnum.ADMIN)
def get_one(conditionnement_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        return get_link(session, conditionnement_id, item_id)
    except ConditionnementItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("", response_model=ConditionnementItemRead)
@is_granted(RoleEnum.ADMIN)
def patch(
    conditionnement_id: int,
    item_id: int,
    payload: ConditionnementItemUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        return update_link(session, conditionnement_id, item_id, payload)
    except ConditionnementItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except QuantityRangeError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete(conditionnement_id: int, item_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    try:
        delete_link(session, conditionnement_id, item_id)
    except ConditionnementItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
