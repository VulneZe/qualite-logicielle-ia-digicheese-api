from typing import List

from sqlmodel import Session

from src.exceptions.unique_entity_exception import UniqueEntityException
from src.models import ZipCode
from src.repositories import ZipCodeRepository
from src.exceptions.not_found_exception import NotFoundException
from src.schemas.zip_code_schema.zip_code_response import ZipCodeResponse
from src.schemas.zip_code_schema.zip_code_create import ZipCodeCreate
from src.schemas.zip_code_schema.zip_code_update import ZipCodeUpdate
from src.services.department_service import DepartmentService


class ZipCodeService:
    def __init__(self, session: Session):
        self.zip_code_repo = ZipCodeRepository(session)
        self.department_service = DepartmentService(session)

    def get_all_zip_codes(self) -> List[ZipCodeResponse] | None:
        collection =  self.zip_code_repo.find_all()
        return collection

    def get_zip_code_by_id(self, zip_code_id: int) -> ZipCodeResponse:
        zip_code = self.zip_code_repo.find(zip_code_id)

        if zip_code is None:
            raise NotFoundException("zip_code not found")

        return zip_code

    def create_zip_code(self, zip_code_data: ZipCodeCreate) -> ZipCode:
        department = self.department_service.get_department_by_id(int(zip_code_data.department_id))

        if department is None:
            raise NotFoundException("Zip Code not found")

        if self.zip_code_repo.find_one_by({"code": zip_code_data.code}):
            raise UniqueEntityException("Code postal existant")

        if not zip_code_data.code.isdigit() or len(zip_code_data.code) != 5:
            raise ValueError("Code postal invalide")

        zip_code = ZipCode(**zip_code_data.model_dump())

        zip_code = self.zip_code_repo.save(zip_code)

        return zip_code

    def update_zip_code(self, zip_code_id: int, zip_code_data: ZipCodeUpdate) -> ZipCodeResponse:
        zip_code = self.get_zip_code_by_id(zip_code_id)

        if self.zip_code_repo.find_one_by({"code": zip_code_data.code}):
            raise UniqueEntityException("Code postal existant")

        for field, value in zip_code_data.model_dump(exclude_unset=True).items():
            setattr(zip_code, field, value)

        return self.zip_code_repo.save(zip_code)

    def delete_zip_code(self, zip_code_id: int) -> None:
        try:
            zip_code = self.get_zip_code_by_id(zip_code_id)
            self.zip_code_repo.remove(zip_code)
        except NotFoundException:
            return