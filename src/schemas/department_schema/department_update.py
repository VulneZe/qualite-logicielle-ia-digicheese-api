from src.models.base import DepartmentBase
from sqlmodel import Field


class DepartmentUpdate(DepartmentBase):
    number: str | None = Field(nullable=False, min_length=2, max_length=3, index=True, unique=True)