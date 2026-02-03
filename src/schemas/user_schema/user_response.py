# Schémas de validation pour les utilisateurs (Pydantic)
from pydantic import Field
from sqlmodel import SQLModel
from datetime import datetime

from src.models.base import UserBase


# Schéma pour les réponses API (données retournées au client)
class UserResponse(UserBase):
    id: int  # ID généré par la base