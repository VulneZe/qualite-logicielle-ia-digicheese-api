# Modèle de base pour les conditionnements
from sqlmodel import SQLModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime

class ConditionnementBase(SQLModel):
    """Modèle de base pour les conditionnements de produits fromagers."""
    
    # Libellé du conditionnement (ex: "Boîte 500g Camembert")
    libelle: str = Field(nullable=False, min_length=2)
    
    # Poids en grammes
    poids: int = Field(nullable=False, gt=0)
    
    # Prix unitaire pour ce conditionnement
    prix: Decimal = Field(nullable=False, gt=0, decimal_places=2)
    
    # Statut actif du conditionnement
    is_active: bool = Field(default=True, nullable=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
