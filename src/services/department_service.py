from typing import List

from sqlmodel import Session

from src.exceptions.unique_entity_exception import UniqueEntityException
from src.models import Department
from src.exceptions.not_found_exception import NotFoundException
from src.repositories.department_repository import DepartmentRepository
from src.schemas.department_schema.DepartmentCreate import DepartmentCreate
from src.schemas.department_schema.department_response import DepartmentResponse
from src.schemas.department_schema.department_update import DepartmentUpdate


class DepartmentService:
    def __init__(self, session: Session):
        self.department_repo = DepartmentRepository(session)

    def get_all_departments(self) -> List[DepartmentResponse] | None:
        collection =  self.department_repo.find_all()
        return collection

    def get_department_by_id(self, department_id: int) -> DepartmentResponse | None:
        department = self.department_repo.find(department_id)

        if department is None:
            raise NotFoundException("Department not found")

        return department

    def create_department(self, department_data: DepartmentCreate) -> DepartmentResponse:
        department = Department(**department_data.model_dump())

        if self.department_repo.find_one_by({"number": department.number}):
            raise UniqueEntityException("Département existant")

        return self.department_repo.save(department)

    def update_department(self, department_id: int, department_data: DepartmentUpdate) -> DepartmentResponse:
        department = self.get_department_by_id(department_id)

        for field, value in department_data.model_dump(exclude_unset=True).items():
            setattr(department, field, value)

        return self.department_repo.save(department)

    def delete_department(self, department_id: int) -> None:
        try:
            department = self.get_department_by_id(department_id)
            self.department_repo.remove(department)
        except NotFoundException:
            return