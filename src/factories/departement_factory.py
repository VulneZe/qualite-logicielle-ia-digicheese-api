from typing import Optional, List
from faker import Faker

from src import Department
from src.factories.interfaces.factories_interface import FactoriesInterface

fake = Faker()

class DepartmentFactory(FactoriesInterface[Department]):

    @classmethod
    def create_one(
            cls,
            session,
            id: Optional[int] = None,
            number: Optional[str] = None,
            **kwargs
    ) -> Department:
        department = Department(number=number or fake.numbertype(nb_digits=2))

        session.add(department)
        session.commit()
        session.refresh(department)
        return department


    @classmethod
    def create_many(cls, session, nb_roles: int = max(1, 5), **kwargs) -> List:
        departments = []
        for _ in range(nb_roles):
            department = cls.create_one(session, **kwargs)
            departments.append(department)
        return departments