from sqlmodel import SQLModel, Field

from src.models.base import ZipCodeBase
from src.schemas.department_schema.department_response import DepartmentResponse


class ZipCodeResponse(ZipCodeBase):
    id: int
    department: DepartmentResponse
