# Repository pour l'accès aux données utilisateurs
from typing import List

from sqlmodel import Session, delete
from .role_repository import RoleRepository
from .. import Role
from ..models import user
from ..models.link import UserRoleLink
from ..models.user import User  # Modèle User
from .abstract import AbstractRepository  # Repository de base

class UserRepository(AbstractRepository[User]):
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
        super().__init__(session, User)
        self.role_repository = RoleRepository(session)

    def add_roles(self, user: User, roles_ids: list[int]):
        # ⚡ Convertir les IDs en int pour éviter les problèmes
        roles_ids = [int(r) for r in roles_ids]

        # Assurer que user est attaché à la session
        self.session.add(user)
        self.session.flush()

        # Utiliser find_by pour récupérer les rôles
        roles_objs = self.role_repository.find_by({"id": {"in": roles_ids}})

        # Vérification des rôles manquants
        if len(roles_objs) != len(roles_ids):
            missing = set(roles_ids) - set(r.id for r in roles_objs)
            raise ValueError(f"Les rôles suivants n'existent pas : {missing}")

        # Créer les UserRoleLink
        for role in roles_objs:
            self.session.add(UserRoleLink(user_id=user.id, role_id=role.id))

    def delete(self, user: User) -> None:
        user.roles.clear()

        self.remove(user)

    def get_user_by_username(self, username: str) -> User | None:
        return self.find_one_by({"username": username})
