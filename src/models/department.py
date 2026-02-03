from typing import List
from sqlmodel import Relationship, Field
from src.models.base import DepartmentBase


class Department(DepartmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    zip_codes: List["ZipCode"] = Relationship(back_populates="department", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all"})