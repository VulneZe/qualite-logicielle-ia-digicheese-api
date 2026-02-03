# Schémas de validation pour les commandes
from pydantic import Field
from sqlmodel import SQLModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.enum.statut_enum import StatutEnum

class CommandeCreate(SQLModel):
    """Schéma pour créer une nouvelle commande."""
    
    # Référence au client (doit exister)
    client_id: int = Field(gt=0)
    
    # Détails de la commande
    statut: StatutEnum = Field(default=StatutEnum.EN_ATTENTE)
    reference: str = Field(min_length=3)
    notes: Optional[str] = Field(default=None)

class CommandeUpdate(SQLModel):
    """Schéma pour modifier une commande existante."""
    
    # Détails modifiables de la commande
    statut: Optional[StatutEnum] = Field(default=None)
    notes: Optional[str] = Field(default=None)

class CommandeResponse(SQLModel):
    """Schéma pour les réponses API."""
    
    id: int
    client_id: int
    date_commande: datetime
    montant_total: Decimal
    statut: StatutEnum
    reference: str
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
