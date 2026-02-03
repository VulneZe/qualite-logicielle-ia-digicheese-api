from sqlmodel import SQLModel
from src.models.base import DepartmentBase

class DepartmentResponse(DepartmentBase):
    id: int
