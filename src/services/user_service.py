# Service métier pour la gestion des utilisateurs
from typing import List

from sqlmodel import Session  # Gestion des sessions base de données

from src.schemas.user_schema.user_response import UserResponse
from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.unique_entity_exception import UniqueEntityException
from src.models.user import User  # Modèle de données User
from src.repositories.role_repository import RoleRepository
from src.repositories.user_repository import UserRepository  # Accès aux données
from src.schemas.user_schema import UserCreate, UserUpdate  # Schémas validation

class UserService:
    """Service pour gérer les utilisateurs : CRUD, hash mots de passe, validation."""
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session) # useer_repository pour accès BDD
        self.role_repository = RoleRepository(session) # role_repository pour accès BDD

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Crée un utilisateur.
        Toute la validation métier est ici.
        """

        # Validation unicité email
        if self.user_repository.find_one_by({"email": user_data.email}):
            raise UniqueEntityException("Email déjà utilisé")

        # Validation unicité username
        if self.user_repository.find_one_by({"username": user_data.username}):
            raise UniqueEntityException("Username déjà utilisé")

        # Hash du password
        data = user_data.model_dump(exclude={"roles_ids"})
        new_user = User(**data)

        try:
            # Sauvegarder l'utilisateur avec les rôles
            self.user_repository.add_roles(new_user, user_data.roles_ids)

            return self.user_repository.save(new_user)
        except Exception as e:
            raise Exception(f"Erreur lors de la création de l'utilisateur : {e}")

    def get_users(self) -> List[UserResponse]:
        """Récupère tous les utilisateurs non-archivés."""
        # Filtre les utilisateurs archivés (suppression logique)
        result = self.user_repository.find_all()
        return result

    def get_user_by_id(self, user_id: int) -> UserResponse | None:
        """Récupère un utilisateur par ID s'il n'est pas archivé."""
        user = self.user_repository.find(user_id)

        if user is None:
            raise NotFoundException("Utilisateur introuvable")

        # Retourne seulement si existe
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        """Met à jour un utilisateur."""
        user = self.user_repository.find(user_id)
        if not user:
            raise NotFoundException("Utilisateur introuvable")

        # Vérifie unicité email et username si changement
        # Validation unicité email
        if self.user_repository.find_one_by({"email": user_data.email}):
            raise UniqueEntityException("Email déjà utilisé")
        # Validation unicité username
        if self.user_repository.find_one_by({"username": user_data.username}):
            raise UniqueEntityException("Username déjà utilisé")

        # Met à jour seulement les champs fournis
        for field, value in user_data.model_dump(exclude_unset=True).items():
            if field == "roles_ids":
                user.roles.clear()
                self.user_repository.add_roles(user, user_data.roles_ids)
            else:
                setattr(user, field, value)

        result = self.user_repository.save(user)
        return result

    def delete_user(self, user_id: int) -> None:
        """Supprime un utilisateur (suppression logique)."""
        try:
            user = self.user_repository.find(user_id)

            self.user_repository.delete(user)
        except NotFoundException:
            return
