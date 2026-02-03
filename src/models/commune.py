# Modèle Commune complet
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from .base.commune_base import CommuneBase

class Commune(CommuneBase, table=True):
    id: int = Field(default=None, primary_key=True)

    zip_code_id: int = Field(foreign_key="zip_code.id")
    zip_code: Optional["ZipCode"] = Relationship(back_populates="communes")

    addresses: Optional["Address"] = Relationship(back_populates="commune")