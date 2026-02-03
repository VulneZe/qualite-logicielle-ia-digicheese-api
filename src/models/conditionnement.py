from typing import Optional
from sqlmodel import Field
from src.models.base.conditionnement_base import ConditionnementBase


class Conditionnement(ConditionnementBase, table=True):
    """Modèle complet pour les conditionnements"""

    id: Optional[int] = Field(default=None, primary_key=True)