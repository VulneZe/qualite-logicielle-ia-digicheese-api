from typing import Optional, List
from faker import Faker

from src import ZipCode
from src.factories.interfaces.factories_interface import FactoriesInterface
from src.models.commune import Commune
from src.schemas.address_schema.address_reponse import AddressResponse
from src.schemas.zip_code_schema.zip_code_response import ZipCodeResponse

fake = Faker()

class CommuneFactory(FactoriesInterface[Commune]):

    @classmethod
    def create_one(
            cls,
            session,
            id: Optional[int] = None,
            nom: Optional[str] = None,
            zip_code: Optional[ZipCodeResponse] = None,
            addresses: Optional[List[AddressResponse]] = None,
            **kwargs
    ) -> Commune:
        commune = Commune(
            nom=nom or fake.city(),
            zip_code=zip_code,
            addresses=addresses or None
        )

        session.add(commune)
        session.commit()
        session.refresh(commune)
        return commune


    @classmethod
    def create_many(cls, session, nb_roles: int = max(1, 5), **kwargs) -> List:
        communes = []
        for _ in range(nb_roles):
            commune = cls.create_one(session, **kwargs)
            communes.append(commune)
        return communes