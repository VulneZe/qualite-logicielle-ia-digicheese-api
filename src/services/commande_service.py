# Service pour la gestion des commandes avec validation des relations Client-Commande
from sqlalchemy.orm import Session
from src.models.commande import Commande
from src.models.client import Client
from src.schemas.commande_schema.commande_schemas import CommandeCreate, CommandeUpdate
from src.repositories.abstract.abstract_repository import ServiceEntityRepository

class CommandeService:
    """Service gérant le cycle de vie des commandes avec validation des relations."""
    
    def __init__(self, session: Session):
        self.repository = ServiceEntityRepository(session, Commande)
        self.client_repository = ServiceEntityRepository(session, Client)
    
    def create_commande(self, commande_data: CommandeCreate) -> Commande:
        """Créer une nouvelle commande avec validation du client."""
        
        # Validation : le client doit exister
        client = self.client_repository.find(commande_data.client_id)
        if not client:
            raise ValueError(f"Client ID {commande_data.client_id} non trouvé")
        
        # Validation : la référence doit être unique
        existing_commande = self.repository.find_one_by({"reference": commande_data.reference})
        if existing_commande:
            raise ValueError(f"Référence '{commande_data.reference}' déjà utilisée")
        
        # Création de la commande avec montant_total par défaut (sera mis à jour par les détails)
        from decimal import Decimal
        commande = Commande(
            client_id=commande_data.client_id,
            montant_total=Decimal('0.00'),  # Par défaut, sera mis à jour par les détails
            statut=commande_data.statut or "en_attente",
            reference=commande_data.reference,
            notes=commande_data.notes
        )
        
        return self.repository.save(commande)
    
    def get_commandes(self, criteria: dict = None) -> list[Commande]:
        """Lister les commandes avec filtres optionnels."""
        if criteria is None:
            criteria = {}
        return self.repository.find_by(criteria)
    
    def get_commande_by_id(self, commande_id: int) -> Commande:
        """Consulter une commande par son ID."""
        commande = self.repository.find(commande_id)
        if not commande:
            raise ValueError(f"Commande ID {commande_id} non trouvée")
        return commande
    
    def get_commandes_by_client(self, client_id: int) -> list[Commande]:
        """Lister toutes les commandes d'un client spécifique."""
        
        # Validation : le client doit exister
        client = self.client_repository.find(client_id)
        if not client:
            raise ValueError(f"Client ID {client_id} non trouvé")
        
        # Récupérer toutes les commandes du client
        return self.repository.find_by({"client_id": client_id})
    
    def update_commande(self, commande_id: int, commande_data: CommandeUpdate) -> Commande:
        """Mettre à jour une commande existante."""
        
        commande = self.get_commande_by_id(commande_id)
        
        # Mise à jour partielle (seulement les champs fournis)
        update_data = commande_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(commande, field, value)
        
        return self.repository.save(commande)
    
    def delete_commande(self, commande_id: int) -> Commande:
        """Supprimer une commande (suppression physique)."""
        commande = self.get_commande_by_id(commande_id)
        return self.repository.delete(commande_id)
