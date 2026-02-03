from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from .personne_base import PersonneBase

class UserBase(PersonneBase):
    email: EmailStr = Field(nullable=False, index=True, unique=True)
    username: str = Field(nullable=False, min_length=5, index=True, unique=True)
    password: str = Field(nullable=False, min_length=12)
    is_active: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
