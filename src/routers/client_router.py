# Routes CRUD pour la gestion des clients avec permissions par rôle
# Ajouté le 19/01/2026 : Sécurisation des endpoints avec @is_granted
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from typing import Optional
from sqlalchemy.orm import Session
from src.config.database import get_session
from src.schemas.client_schema.client_schemas import ClientCreate, ClientUpdate, ClientResponse
from src.security.auth import get_current_user
from src.services.client_service import ClientService
from src.enum.role_enum import RoleEnum
from src.security.guard.role_gard_decorator import is_granted

clients = APIRouter()

@clients.post("/", response_model=ClientResponse, status_code=201)
@is_granted(RoleEnum.OP_COLIS)  # PERMISSION: Admin + Opérateur Colis peuvent créer des clients
def create_client(client_data: ClientCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Créer un nouveau client.
    Permissions requises: ADMIN ou OP_COLIS
    - ADMIN: Peut créer des clients (gestion complète)
    - OP_COLIS: Peut créer des clients (gestion des commandes)
    """
    service = ClientService(session)
    return service.create_client(client_data)

@clients.get("/", response_model=list[ClientResponse])
@is_granted(RoleEnum.OP_COLIS)  # PERMISSION: Tous les rôles peuvent voir les clients
def get_clients(
    nom: Optional[str] = Query(None),
    ville: Optional[str] = Query(None),
    code_postal: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Lister tous les clients avec filtres optionnels.
    Permissions requises: ADMIN, OP_COLIS ou OP_STOCK
    - ADMIN: Accès complet à tous les clients
    - OP_COLIS: Peut voir les clients pour gérer les commandes
    """
    service = ClientService(session)
    
    criteria = {}
    if nom:
        criteria["nom"] = f"%{nom}%"
    if ville:
        criteria["ville"] = ville
    if code_postal:
        criteria["code_postal"] = code_postal
    
    return service.get_clients(criteria)

@clients.get("/{client_id}", response_model=ClientResponse)
@is_granted(RoleEnum.OP_COLIS)  # PERMISSION: Tous les rôles peuvent voir un client spécifique
def get_client(client_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Consulter les détails d'un client par son ID.
    Permissions requises: ADMIN, OP_COLIS ou OP_STOCK
    - ADMIN: Accès complet à tous les clients
    - OP_COLIS: Peut voir les clients pour gérer les commandes
    """
    service = ClientService(session)
    return service.get_client_by_id(client_id)

@clients.patch("/{client_id}", response_model=ClientResponse)
@is_granted(RoleEnum.OP_COLIS)  # PERMISSION: Admin + Opérateur Colis peuvent modifier des clients
def update_client(
    client_id: int, 
    client_data: ClientUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Mettre à jour un client existant.
    Permissions requises: ADMIN ou OP_COLIS
    - ADMIN: Peut modifier tous les clients (gestion complète)
    - OP_COLIS: Peut modifier les clients (gestion des commandes)
    """
    service = ClientService(session)
    return service.update_client(client_id, client_data)

@clients.delete("/{client_id}")
@is_granted(RoleEnum.OP_COLIS)  # PERMISSION: Admin + Opérateur Colis peuvent supprimer des clients
def delete_client(client_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Supprimer un client.
    Permissions requises: ADMIN ou OP_COLIS
    - ADMIN: Peut supprimer tous les clients (gestion complète)
    - OP_COLIS: Peut supprimer les clients (gestion des commandes)
    """
    service = ClientService(session)
    if not service.delete_client(client_id):
        raise HTTPException(status_code=404, detail="Client introuvable")
    return {"message": "Client supprimé"}
