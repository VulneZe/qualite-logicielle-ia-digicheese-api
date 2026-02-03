# Routes CRUD pour la gestion des communes
# Ajouté le 19/01/2026 : Sécurisation des endpoints avec @is_granted
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from src.config.database import get_session
from src.schemas.commune_schema.commune_schemas import CommuneCreate, CommuneUpdate, CommuneResponse
from src.security.auth import get_current_user
from src.services.commune_service import CommuneService
from src.enum.role_enum import RoleEnum
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter()

@router.post("/", response_model=CommuneResponse, status_code=201)
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut créer des communes
def create_commune(commune_data: CommuneCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)) -> CommuneResponse:
    """
    Créer une nouvelle commune.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut créer des communes (gestion complète)
    - OP_COLIS: Ne peut PAS créer de communes (accès lecture seule)
    """
    service = CommuneService(session)
    return service.create_commune(commune_data)

@router.get("/", response_model=list[CommuneResponse])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)  # PERMISSION: Tous les rôles peuvent voir les communes
def get_communes(current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Lister toutes les communes.
    Permissions requises: ADMIN, OP_COLIS ou OP_STOCK
    - ADMIN: Accès complet à toutes les communes
    - OP_COLIS: Peut voir les communes (consultation)
    """
    service = CommuneService(session)
    return service.get_communes()

@router.get("/{commune_id}", response_model=CommuneResponse)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)  # PERMISSION: Tous les rôles peuvent voir une commune spécifique
def get_commune(commune_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Consulter les détails d'une commune par son ID.
    Permissions requises: ADMIN, OP_COLIS ou OP_STOCK
    - ADMIN: Accès complet à toutes les communes
    - OP_COLIS: Peut voir les communes (consultation)
    """
    service = CommuneService(session)
    return service.get_commune_by_id(commune_id)

@router.patch("/{commune_id}", response_model=CommuneResponse)
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut modifier des communes
def update_commune(commune_id: int, commune_data: CommuneUpdate, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Mettre à jour une commune existante.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut modifier des communes (gestion complète)
    - OP_COLIS: Ne peut PAS modifier de communes (accès lecture seule)
    """
    service = CommuneService(session)
    return service.update_commune(commune_id, commune_data)

@router.delete("/{commune_id}")
@is_granted(RoleEnum.ADMIN)  # PERMISSION: Seul l'Admin peut supprimer des communes
def delete_commune(commune_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Supprimer une commune.
    Permissions requises: ADMIN uniquement
    - ADMIN: Peut supprimer des communes (gestion complète)
    - OP_COLIS: Ne peut PAS supprimer de communes (accès lecture seule)
    """
    service = CommuneService(session)
    service.delete_commune(commune_id)
    return {"message": "Commune supprimée"}
