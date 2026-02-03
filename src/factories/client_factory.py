from datetime import datetime
from typing import List, Optional
from faker import Faker

from src.models.client import Client
from .interfaces.factories_interface import FactoriesInterface
from ..schemas.address_schema.address_reponse import AddressResponse

fake = Faker()


class ClientFactory(FactoriesInterface[Client]):
    """Factory pour créer des clients avec SQLModel."""

    @classmethod
    def create_one(
        cls,
        session,
        id: Optional[int] = None,
        nom: Optional[str] = None,
        prenom: Optional[str] = None,
        email: Optional[str] = None,
        telephone: Optional[str] = None,
        address: Optional[AddressResponse] = None,
        address_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        created_at: datetime = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> Client:
        """Crée un seul client et l'ajoute à la session."""

        client = Client(
            nom=nom or fake.last_name(),
            prenom=prenom or fake.first_name(),
            email=email or fake.email(),
            telephone=telephone or fake.phone_number(),
            address_id=address.id if address else None,
            adresse=address,
            is_active=True
        )

        session.add(client)
        session.commit()
        session.refresh(client)

        return client

    @classmethod
    def create_many(cls, session, nb_clients: int = 5, **kwargs) -> List:
        """Crée plusieurs clients."""
        clients = []
        for _ in range(nb_clients):
            client = cls.create_one(session, **kwargs)
            clients.append(client)
        return clients