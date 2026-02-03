# Routes CRUD pour la gestion des utilisateurs
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session

from src import RoleEnum
from src.config.database import get_session  # Connexion à la base de données
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.unique_entity_exception import UniqueEntityException
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted
from src.services.user_service import UserService  # Logique métier utilisateur
from src.schemas.user_schema import UserCreate, UserUpdate, UserResponse  # Schémas de validation


# users pour les endpoints utilisateurs avec préfixe /users
users = APIRouter()

@users.post("/",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create_user(user_data: UserCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    user_service = UserService(session)

    try:
        user = user_service.create_user(user_data)
        return UserResponse.model_validate(user)

    except UniqueEntityException as e:
        raise HTTPException(status_code=409, detail=str(e))

@users.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_users(current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> List[UserResponse]:
    """Récupère liste utilisateurs via GET."""
    user_service = UserService(session)
    try:
        return user_service.get_users()  # Liste non-archivés
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne

@users.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_user(user_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> UserResponse:
    """Récupère utilisateur par ID via GET."""
    service = UserService(session)
    try:
        user = service.get_user_by_id(user_id)  # Cherche par ID
        return UserResponse.model_validate(user)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne

@users.patch("/{user_id}", response_model=UserResponse)
@is_granted(RoleEnum.ADMIN)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_user=Depends(get_current_user),
        session: Session = Depends(get_session)
) -> UserResponse:
    """Met à jour utilisateur via PATCH."""
    service = UserService(session)
    try:
        user = service.update_user(user_id, user_data)  # Met à jour
        return UserResponse.model_validate(user)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne

@users.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_user(user_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> None:
    """Supprime utilisateur via DELETE."""
    service = UserService(session)
    try:
        service.delete_user(user_id) # Supprime si existe
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne