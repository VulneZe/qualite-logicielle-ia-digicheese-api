from typing import Optional, List
from faker import Faker

from src import ZipCode
from src.factories.interfaces.factories_interface import FactoriesInterface
from src.schemas.department_schema.department_response import DepartmentResponse

fake = Faker()

class ZipCodeFactory(FactoriesInterface[ZipCode]):

    @classmethod
    def create_one(
        cls,
        session,
        id: Optional[int] = None,
        code: Optional[str] = None,
        department: Optional[DepartmentResponse] = None,
        **kwargs,
    ) -> ZipCode:
        zip_code = ZipCode(code=code or fake.postcode(), department=department)

        session.add(zip_code)
        session.commit()
        session.refresh(zip_code)
        return zip_code


    @classmethod
    def create_many(cls, session, nb_roles: int = max(1, 5), **kwargs) -> List:
        zip_codes = []
        for _ in range(nb_roles):
            zip_code = cls.create_one(session, **kwargs)
            zip_codes.append(zip_code)
        return zip_codes