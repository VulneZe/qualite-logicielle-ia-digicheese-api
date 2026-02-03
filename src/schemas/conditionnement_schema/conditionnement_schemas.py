# Schémas pour les conditionnements
from pydantic import Field
from sqlmodel import SQLModel
from decimal import Decimal
from typing import Optional
from datetime import datetime

class ConditionnementCreate(SQLModel):
    """Schéma pour créer un conditionnement."""
    
    libelle: str = Field(min_length=2, description="Libellé du conditionnement")
    poids: int = Field(gt=0, description="Poids en grammes")
    prix: Decimal = Field(gt=0, decimal_places=2, description="Prix unitaire")

class ConditionnementUpdate(SQLModel):
    """Schéma pour mettre à jour un conditionnement."""
    
    libelle: Optional[str] = Field(default=None, min_length=2)
    poids: Optional[int] = Field(default=None, gt=0)
    prix: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    is_active: Optional[bool] = Field(default=None)

class ConditionnementResponse(SQLModel):
    """Schéma pour les réponses API."""
    
    id: int
    libelle: str
    poids: int
    prix: Decimal
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
