from sqlalchemy.orm import Session

from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.unique_entity_exception import UniqueEntityException
from src.models.commune import Commune
from src.schemas.commune_schema.commune_schemas import CommuneCreate, CommuneUpdate
from src.repositories.abstract.abstract_repository import ServiceEntityRepository
from src.services.zip_code_service import ZipCodeService


class CommuneService:
    def __init__(self, session: Session):
        self.repository = ServiceEntityRepository(session, Commune)
        self.zip_code_service = ZipCodeService(session)
    
    def create_commune(self, commune_data: CommuneCreate) -> Commune:
        zip_code = self.zip_code_service.get_zip_code_by_id(commune_data.zip_code_id)

        if not zip_code:
            raise NotFoundException("Zip Code invalide")

        if self.repository.find_one_by({"nom": commune_data.nom, "zip_code": zip_code}):
            raise ValueError("Commune déjà existante")
        
        commune = Commune(**commune_data.model_dump())

        commune = self.repository.save(commune)
        
        return commune
    
    def get_communes(self) -> list[Commune]:
        return self.repository.find_by({})
    
    def get_commune_by_id(self, commune_id: int) -> Commune:
        commune = self.repository.find(commune_id)
        if not commune:
            raise ValueError("Commune non trouvée")
        return commune
    
    def update_commune(self, commune_id: int, commune_data: CommuneUpdate) -> Commune:
        commune = self.get_commune_by_id(commune_id)

        if commune is None:
            raise NotFoundException("Commune invalide")

        if commune_data.nom == commune.nom and commune_data.zip_code_id == commune.zip_code_id:
            raise UniqueEntityException("Commune déjà existante")
        
        for field, value in commune_data.model_dump(exclude_unset=True).items():
            setattr(commune, field, value)
        
        return self.repository.save(commune)
    
    def delete_commune(self, commune_id: int) -> Commune:
        commune = self.get_commune_by_id(commune_id)
        return self.repository.delete(commune_id)
