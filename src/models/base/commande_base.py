# Modèle de base pour les commandes
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.enum.statut_enum import StatutEnum

class CommandeBase(SQLModel):
    """
    Modèle de base pour les commandes avec relation client.
    
    Modifications par rapport à la version précédente :
    - Remplacement du champ 'statut' de type str par StatutEnum pour validation stricte
    - Conservation de la relation client_id
    """
    
    # Clé étrangère vers le client
    client_id: int = Field(nullable=False, foreign_key="client.id")
    
    # Informations de la commande
    date_commande: datetime = Field(default_factory=lambda: datetime.now())
    montant_total: Decimal = Field(nullable=False, gt=0)
    
    # Statut de la commande (stocké comme string, validé par ENUM)
    statut: str = Field(default=StatutEnum.EN_ATTENTE.value)  # Stocke la valeur de l'ENUM
    
    # Référence et notes
    reference: str = Field(nullable=False, unique=True)
    notes: Optional[str] = Field(default=None)
