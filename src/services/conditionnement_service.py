# Service pour la gestion des conditionnements
from sqlmodel import Session, select
from typing import List, Optional
from src.models.conditionnement import Conditionnement
from src.schemas.conditionnement_schema.conditionnement_schemas import (
    ConditionnementCreate,
    ConditionnementUpdate
)

class ConditionnementService:
    """Service pour la gestion des conditionnements."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_conditionnements(self) -> List[Conditionnement]:
        """Récupérer tous les conditionnements actifs."""
        statement = select(Conditionnement).where(Conditionnement.is_active == True)
        return self.session.exec(statement).all()
    
    def get_conditionnement_by_id(self, conditionnement_id: int) -> Optional[Conditionnement]:
        """Récupérer un conditionnement par son ID."""
        return self.session.get(Conditionnement, conditionnement_id)
    
    def create_conditionnement(self, conditionnement_data: ConditionnementCreate) -> Conditionnement:
        """Créer un nouveau conditionnement."""
        conditionnement = Conditionnement(**conditionnement_data.dict())
        self.session.add(conditionnement)
        self.session.commit()
        self.session.refresh(conditionnement)
        return conditionnement
    
    def update_conditionnement(
        self, 
        conditionnement_id: int, 
        conditionnement_data: ConditionnementUpdate
    ) -> Optional[Conditionnement]:
        """Mettre à jour un conditionnement."""
        conditionnement = self.session.get(Conditionnement, conditionnement_id)
        if not conditionnement:
            return None
        
        update_data = conditionnement_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conditionnement, field, value)
        
        self.session.add(conditionnement)
        self.session.commit()
        self.session.refresh(conditionnement)
        return conditionnement
    
    def delete_conditionnement(self, conditionnement_id: int) -> bool:
        """Supprimer un conditionnement (désactivation)."""
        conditionnement = self.session.get(Conditionnement, conditionnement_id)
        if not conditionnement:
            return False
        
        conditionnement.is_active = False
        self.session.add(conditionnement)
        self.session.commit()
        return True
