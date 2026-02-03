from sqlalchemy.orm import Session
from src.models.address import Address
from src.models.client import Client
from src.schemas.client_schema.client_schemas import ClientCreate, ClientUpdate, ClientResponse
from .commune_service import CommuneService
from datetime import datetime

from .. import ZipCodeRepository, CommuneRepository, CommandeRepository, AddressRepository
from ..exceptions.not_found_exception import NotFoundException
from ..exceptions.unique_entity_exception import UniqueEntityException
from ..repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, session: Session):
        self.client_repo = ClientRepository(session)
        self.zip_code_repo = ZipCodeRepository(session)
        self.commune_service = CommuneService(session)
        self.commune_repo = CommuneRepository(session)
        self.commande_repository = CommandeRepository(session)
        self.address_repository = AddressRepository(session)
    
    def create_client(self, client_data: ClientCreate) -> ClientResponse:
        if self.client_repo.find_one_by({"email": client_data.email}):
            raise UniqueEntityException("Email déjà utilisé")
        
        if client_data.address.commune_id:
            commune = self.commune_repo.find(client_data.address.commune_id)
            if not commune:
                raise NotFoundException("Commune invalide ou inexistante")

        if client_data.address.zip_code_id:
            zip_code = self.zip_code_repo.find(client_data.address.zip_code_id)
            if not zip_code:
                raise NotFoundException("Zip Code invalide ou inexistante")

        if client_data.address is None:
            raise NotFoundException("Adresse invalide ou inexistante")

        address = Address(
            address=client_data.address.address,
            address_complement_first=client_data.address.address_complement_first or None,
            address_complement_second=client_data.address.address_complement_second or None,
            zip_code_id=client_data.address.zip_code_id,
            commune_id=client_data.address.commune_id
        )

        self.address_repository.session.add(address)
        self.address_repository.session.flush()
        
        client = Client(
            nom=client_data.nom,
            prenom=client_data.prenom,
            email=client_data.email,
            telephone=client_data.telephone or None,
            address=address
        )

        client = self.client_repo.save(client)

        self.client_repo.session.refresh(client.address)
        
        return client
    
    def get_clients(self, criteria: dict = None) -> list[Client]:
        if criteria is None:
            criteria = {}
        
        return self.client_repo.find_by(criteria)
    
    def get_client_by_id(self, client_id: int) -> Client:
        client = self.client_repo.find(client_id)
        if not client:
            raise NotFoundException("Client non trouvé")
        return client

    def update_client(self, client_id: int, client_data: ClientUpdate) -> Client:
        # Récupère le client et l'adresse existante
        client = self.get_client_by_id(client_id)
        address = self.address_repository.find(client.address.id)

        # Vérifie email unique
        if client_data.email and client_data.email != client.email:
            if self.client_repo.find_one_by({"email": client_data.email}):
                raise ValueError("Email déjà utilisé")

        for field, value in client_data.address.model_dump(exclude_unset=True).items():
            setattr(address, field, value)

        self.address_repository.session.flush()

        for field, value in client_data.model_dump(exclude_unset=True).items():
            if field != "address":
                setattr(client, field, value)

        client.updated_at = datetime.now()

        client = self.client_repo.save(client)

        self.client_repo.session.refresh(client)
        self.client_repo.session.refresh(client.address)

        return client



    def delete_client(self, client_id: int) -> bool:
        """Supprimer un client avec validation des commandes."""
        client = self.get_client_by_id(client_id)
        
        # Vérifier si le client a des commandes
        commandes = self.commande_repository.find_by({"client_id": client_id})
        if commandes:
            client.is_active = False
            self.client_repo.save(client)

        self.client_repo.delete(client_id)
        
        return True
