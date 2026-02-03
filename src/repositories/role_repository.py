# Repository pour l'accès aux données roles
from sqlmodel import Session

from ..models.role import Role
from .abstract import AbstractRepository  # Repository de base

class RoleRepository(AbstractRepository[Role]):
    """
    Repository spécialisé pour les utilisateurs.

    Hérite de ServiceEntityRepository qui fournit :
    - find(id) : trouver par ID
    - find_one_by(criteria) : trouver par critère
    - find_all() : tous les enregistrements
    - find_by(criteria, order_by, limit, offset) : recherche avancée
    - save(entity) : sauvegarder
    - remove(entity) : supprimer
    """

    def __init__(self, session: Session):
        # Initialise le repository avec le modèle User
        super().__init__(session, Role)