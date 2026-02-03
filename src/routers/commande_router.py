# Routes CRUD pour la gestion des commandes avec relation Client-Commande
# Ajouté le 19/01/2026 : Sécurisation des endpoints avec @is_granted
from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from src.config.database import get_session
from src.schemas.commande_schema.commande_schemas import CommandeCreate, CommandeUpdate, CommandeResponse
from src.services.commande_service import CommandeService
from src.enum.role_enum import RoleEnum
from src.security.guard.role_gard_decorator import is_granted

router = APIRouter()

@router.post("/", response_model=CommandeResponse, status_code=201)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)  # PERMISSION: Admin + Opérateur Colis peuvent créer des commandes
def create_commande(commande_data: CommandeCreate, session: Session = Depends(get_session)):
    """
    Créer une nouvelle commande.
    Permissions requises: ADMIN ou OP_COLIS
    - ADMIN: Peut créer des commandes (gestion complète)
    - OP_COLIS: Peut créer des commandes (gestion des colis)
    - OP_STOCK: Ne peut PAS créer de commandes (accès lecture seule)
    """
    service = CommandeService(session)
    return service.create_commande(commande_data)

@router.get("/", response_model=list[CommandeResponse])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)  # PERMISSION: Tous les rôles peuvent voir les commandes
def get_commandes(
    client_id: Optional[int] = Query(None),
    statut: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    """
    Lister toutes les commandes avec filtres optionnels.
    Permissions requises: ADMIN, OP_COLIS ou OP_STOCK
    - ADMIN: Accès complet à toutes les commandes
    - OP_COLIS: Peut voir les commandes (gestion des colis)
    - OP_STOCK: Peut voir les commandes (consultation)
    """
    service = CommandeService(session)
    
    criteria = {}
    if client_id:
        criteria["client_id"] = client_id
    if statut:
        criteria["statut"] = statut
    
    return service.get_commandes(criteria)

@router.get("/{commande_id}", response_model=CommandeResponse)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
def get_commande(commande_id: int, session: Session = Depends(get_session)):
    """Consulter les détails d'une commande par son ID."""
    service = CommandeService(session)
    return service.get_commande_by_id(commande_id)

@router.get("/client/{client_id}", response_model=list[CommandeResponse])
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS, RoleEnum.OP_STOCK)
def get_commandes_by_client(client_id: int, session: Session = Depends(get_session)):
    """Lister toutes les commandes d'un client spécifique."""
    service = CommandeService(session)
    return service.get_commandes_by_client(client_id)

@router.patch("/{commande_id}", response_model=CommandeResponse)
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def update_commande(
    commande_id: int, 
    commande_data: CommandeUpdate, 
    session: Session = Depends(get_session)
):
    """Mettre à jour une commande existante."""
    service = CommandeService(session)
    return service.update_commande(commande_id, commande_data)

@router.delete("/{commande_id}")
@is_granted(RoleEnum.ADMIN, RoleEnum.OP_COLIS)
def delete_commande(commande_id: int, session: Session = Depends(get_session)):
    """Supprimer une commande (suppression physique)."""
    service = CommandeService(session)
    service.delete_commande(commande_id)
    return {"message": "Commande supprimée"}
