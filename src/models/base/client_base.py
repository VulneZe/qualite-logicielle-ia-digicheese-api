# Modèle de base pour les clients
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ClientBase(SQLModel):
    """
    Modèle de base pour les clients.
    
    Modifications par rapport à la version précédente :
    - Suppression des champs 'code_postal' et 'ville' (remplacés par référence via commune_id)
    - Conservation de 'commune_id' pour la relation avec la table commune
    """
    
    # Informations personnelles obligatoires
    nom: str = Field(nullable=False, min_length=2)
    prenom: str = Field(nullable=False, min_length=2)
    email: str = Field(nullable=False, min_length=5)
    
    # Informations de contact optionnelles
    telephone: Optional[str] = Field(default=None)

    # Statut et timestamps
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
