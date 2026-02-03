from typing import Optional, List
from pydantic import EmailStr, BaseModel, Field, field_validator

from src.validators.validator import Validator
from src.security.auth import Auth

# Schéma pour créer un nouvel utilisateur (validation des données d'entrée)
class UserCreate(BaseModel):
    last_name: str = Field(min_length=2)  # Nom minimum 2 caractères
    first_name: str = Field(min_length=2)  # Prénom minimum 2 caractères
    email: EmailStr # Email valide automatiquement
    username: str = Field(min_length=5)  # Pseudo minimum 5 caractères
    password: str = Field(min_length=12)  # Mot de passe minimum 12 caractères
    is_active: Optional[bool] = Field(default=False)  # Compte inactif par défaut
    roles_ids: List[int] = Field(..., description="Liste des IDs des rôles assignés")

    @classmethod
    @field_validator('password')
    def validate_password(cls, plain_password: str):
        return Validator.validate_password(plain_password)

    @field_validator('password')
    def password_hash(cls, plain_password: str) -> str:
        return Auth.password_hash(plain_password)

    @classmethod
    @field_validator('email')
    def validate_email(cls, email: str) -> str :
        return Validator.validate_email(email)