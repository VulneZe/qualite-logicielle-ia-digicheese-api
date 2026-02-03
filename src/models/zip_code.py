from typing import List, Optional

from src.models.base import ZipCodeBase
from sqlmodel import Field, Relationship

from src.models.commune import Commune
from src.models.department import Department
from src.models.address import Address


class ZipCode(ZipCodeBase, table=True):
    __tablename__ = "zip_code"

    id: int | None = Field(default=None, primary_key=True)

    department_id: int = Field(foreign_key="department.id")
    department: Optional["Department"] = Relationship(back_populates="zip_codes")

    addresses: List["Address"] = Relationship(back_populates="zip_code")
    communes: List["Commune"] = Relationship(back_populates="zip_code")
