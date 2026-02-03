from pydantic import EmailStr, Field, field_validator
from sqlmodel import SQLModel
from typing import Optional, List

from src.validators.validator import Validator
from src.security.auth import Auth


# Schéma pour mettre à jour un utilisateur (champs optionnels)
class UserUpdate(SQLModel):
    last_name: Optional[str] = Field(min_length=2, default=None)
    first_name: Optional[str] = Field(min_length=2, default=None)
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(min_length=5, default=None)
    password: Optional[str] = Field(min_length=12, default=None)  # Nouveau mot de passe si modifié
    is_active: Optional[bool] = None  # Activer/désactiver compte
    roles_ids: List[int] | None = None

    @classmethod
    @field_validator('password')
    def validate_password(cls, plain_password: str) -> str :
        return Validator.validate_password(plain_password)

    @field_validator('password')
    def password_hash(cls, plain_password: str) -> str:
        return Auth.password_hash(plain_password)

    @classmethod
    @field_validator('email')
    def validate_email(cls, email: str) -> str :
        return Validator.validate_email(email)