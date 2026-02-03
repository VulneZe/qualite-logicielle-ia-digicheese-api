# Modèle Client complet
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from .base.client_base import ClientBase
from .. import Address


class Client(ClientBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
    # Relations
    commandes: list["Commande"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    address_id: int = Field(foreign_key="address.id", unique=True)
    address: Optional[Address] = Relationship(back_populates="client")

