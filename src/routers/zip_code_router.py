# Routes CRUD pour la gestion des departement
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session

from src import RoleEnum
from src.config.database import get_session  # Connexion à la base de données
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.unique_entity_exception import UniqueEntityException
from src.schemas.zip_code_schema.zip_code_create import ZipCodeCreate
from src.schemas.zip_code_schema.zip_code_response import ZipCodeResponse
from src.schemas.zip_code_schema.zip_code_update import ZipCodeUpdate
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted
from src.services.zip_code_service import ZipCodeService  # Logique métier utilisateur


# users pour les endpoints departement avec préfixe /users
zip_codes = APIRouter()

@zip_codes.post("/",response_model=ZipCodeResponse, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create_zip_code(zip_code_data: ZipCodeCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> ZipCodeResponse:

    try:
        zip_code_service = ZipCodeService(session)

        zip_code = zip_code_service.create_zip_code(zip_code_data)
        return ZipCodeResponse.model_validate(zip_code)
    except UniqueEntityException as e:
        raise HTTPException(status_code=409, detail=str(e))

@zip_codes.get("/", response_model=list[ZipCodeResponse], status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_zip_codes(current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> List[ZipCodeResponse] | List:
    """Récupère liste zipCode via GET."""
    zip_code_service = ZipCodeService(session)
    departments = zip_code_service.get_all_zip_codes()
    return departments or []

@zip_codes.get("/{zip_code_id}", response_model=ZipCodeResponse, status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_zip_code(zip_code_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> ZipCodeResponse:
    """Récupère zipCode par ID via GET."""
    service = ZipCodeService(session)
    try:
        zip_code = service.get_zip_code_by_id(zip_code_id)  # Cherche par ID
        return ZipCodeResponse.model_validate(zip_code)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne

@zip_codes.patch("/{zip_code_id}", response_model=ZipCodeResponse)
@is_granted(RoleEnum.ADMIN)
def update_zip_code(
        zip_code_id: int,
        zip_code_data: ZipCodeUpdate,
        current_user=Depends(get_current_user),
        session: Session = Depends(get_session)
) -> ZipCodeResponse:
    """Met à jour zipCode via PATCH."""
    try:
        service = ZipCodeService(session)
        zip_code = service.update_zip_code(zip_code_id, zip_code_data)  # Met à jour
        return ZipCodeResponse.model_validate(zip_code)
    except UniqueEntityException as e:
        raise HTTPException(status_code=409, detail=str(e))

@zip_codes.delete("/{zip_code_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_zip_code(zip_code_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> None:
    """Supprime zipCode via DELETE."""
    service = ZipCodeService(session)
    service.delete_zip_code(zip_code_id) # Supprime si existe
