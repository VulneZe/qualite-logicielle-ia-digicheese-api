import datetime
from typing import List, Optional
from faker import Faker

from .interfaces.factories_interface import FactoriesInterface
from .. import Address

fake = Faker()

class AddressFactory(FactoriesInterface[Address]):
    """Factory pour créer des adresses avec SQLModel."""

    @classmethod
    def create_one(
        cls,
        session,
        address: Optional[str] = None,
        address_complement_first: Optional[str] | None = None,
        address_complement_second: Optional[str] | None = None,
        zip_code_id: Optional[int] = None,
        commune_id: Optional[int] = None,
        **kwargs,
    ) -> Address:
        """Crée un seule clienadresset et l'ajoute à la session."""

        address = Address(
            address=address or fake.address(),
            address_complement_first=address_complement_first or None,
            address_complement_second=address_complement_second or None,
            zip_code_id=zip_code_id,
            commune_id=commune_id
        )

        session.add(address)
        session.commit()
        session.refresh(address)

        return address

    @classmethod
    def create_many(cls, session, nb_addresses: int = 5, **kwargs) -> List[Address]:
        """Crée plusieurs adresses."""
        addresses = []
        for _ in range(nb_addresses):
            address = cls.create_one(session, **kwargs)
            addresses.append(address)
        return addresses