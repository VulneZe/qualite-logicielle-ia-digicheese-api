from typing import Optional

from .user import User
from src.models.base import AddressBase
from sqlmodel import Field, Relationship


class Address(AddressBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    zip_code_id: int = Field(foreign_key="zip_code.id")
    zip_code: Optional["ZipCode"] = Relationship(back_populates="addresses")

    commune_id: int = Field(foreign_key="commune.id")
    commune: Optional["Commune"] = Relationship(back_populates="addresses")

    client: Optional["Client"] = Relationship(back_populates="address", sa_relationship_kwargs={"uselist": False})
