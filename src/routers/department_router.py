# Routes CRUD pour la gestion des departement
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session

from src import RoleEnum
from src.config.database import get_session  # Connexion à la base de données
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.unique_entity_exception import UniqueEntityException
from src.schemas.department_schema.DepartmentCreate import DepartmentCreate
from src.schemas.department_schema.department_response import DepartmentResponse
from src.schemas.department_schema.department_update import DepartmentUpdate
from src.security.auth import get_current_user
from src.security.guard.role_gard_decorator import is_granted
from src.services.department_service import DepartmentService  # Logique métier utilisateur


# users pour les endpoints departement avec préfixe /users
departements = APIRouter()

@departements.post("/",response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
@is_granted(RoleEnum.ADMIN)
def create_department(department_data: DepartmentCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    department_service = DepartmentService(session)

    department = department_service.create_department(department_data)
    return DepartmentResponse.model_validate(department)

@departements.get("/", response_model=list[DepartmentResponse], status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_departments(current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> List[DepartmentResponse] | List:
    """Récupère liste departement via GET."""
    department_service = DepartmentService(session)
    departments = department_service.get_all_departments()
    return departments or []

@departements.get("/{department_id}", response_model=DepartmentResponse, status_code=status.HTTP_200_OK)
@is_granted(RoleEnum.ADMIN)
def get_department(department_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> DepartmentResponse:
    """Récupère utilisateur par ID via GET."""
    service = DepartmentService(session)
    try:
        department = service.get_department_by_id(department_id)  # Cherche par ID
        return DepartmentResponse.model_validate(department)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # Erreur interne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Erreur interne

@departements.patch("/{department_id}", response_model=DepartmentResponse)
@is_granted(RoleEnum.ADMIN)
def update_department(
        department_id: int,
        department_data: DepartmentUpdate,
        current_user=Depends(get_current_user),
        session: Session = Depends(get_session)
) -> DepartmentResponse:
    """Met à jour depoartement via PATCH."""
    service = DepartmentService(session)
    department = service.update_department(department_id, department_data)  # Met à jour
    return DepartmentResponse.model_validate(department)

@departements.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_granted(RoleEnum.ADMIN)
def delete_department(department_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> None:
    """Supprime departement via DELETE."""
    service = DepartmentService(session)
    service.delete_department(department_id) # Supprime si existe
