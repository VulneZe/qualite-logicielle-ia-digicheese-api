# Schémas de validation pour les clients
from pydantic import Field, EmailStr
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional

from src.schemas.address_schema.address_create import AddressCreate
from src.schemas.address_schema.address_reponse import AddressResponse
from src.schemas.address_schema.address_update import AddressUpdate


class ClientCreate(SQLModel):
    """
    Schéma pour créer un nouveau client.
    
    Modifications par rapport à la version précédente :
    - Suppression des champs 'code_postal' et 'ville' (remplacés par commune_id)
    - Conservation de 'commune_id' pour la relation avec la table commune
    """
    
    # Informations personnelles obligatoires
    nom: str = Field(min_length=2)
    prenom: str = Field(min_length=2)
    email: EmailStr = Field(min_length=5)

    # Informations de contact optionnelles
    telephone: Optional[str] = Field(default=None)
    address: AddressCreate
    # Statut
    is_active: Optional[bool] = Field(default=True)

class ClientUpdate(SQLModel):
    """
    Schéma pour modifier un client existant.
    
    Modifications par rapport à la version précédente :
    - Suppression des champs 'code_postal' et 'ville' (remplacés par commune_id)
    - Conservation de 'commune_id' pour la relation avec la table commune
    """
    
    # Informations personnelles optionnelles
    nom: Optional[str] = Field(min_length=2, default=None)
    prenom: Optional[str] = Field(min_length=2, default=None)
    email: Optional[EmailStr] = Field(min_length=5, default=None)
    
    # Informations de contact optionnelles
    telephone: Optional[str] = Field(default=None)
    address: Optional[AddressUpdate] = Field(default=None)

# Statut
    is_active: Optional[bool] = Field(default=None)

class ClientResponse(SQLModel):
    """
    Schéma pour les réponses API (retour des données client).
    
    Modifications par rapport à la version précédente :
    - Suppression des champs 'code_postal' et 'ville' (remplacés par commune_id)
    - Conservation de 'commune_id' pour la relation avec la table commune
    """
    
    id: int
    nom: str
    prenom: str
    email: str
    telephone: Optional[str]
    address: AddressResponse
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
