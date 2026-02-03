# Modèle Commande complet
from typing import List, Optional
from sqlmodel import Relationship, Field
from src.models.base.commande_base import CommandeBase
from src.models.client import Client

class Commande(CommandeBase, table=True):
    """Modèle Commande complet avec relation vers Client."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relation avec la table Client (une commande appartient à un seul client)
    client: Optional['Client'] = Relationship(back_populates='commandes')

