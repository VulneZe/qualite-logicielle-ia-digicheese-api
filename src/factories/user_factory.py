from typing import Optional, List
from faker import Faker
from pydantic import field_validator

from src import Auth, UserCreate
from src.factories.interfaces.factories_interface import FactoriesInterface
from src.models.user import User
from src.factories.role_factory import RoleFactory

fake = Faker()


class UserFactory(FactoriesInterface[User]):
    """Factory générique pour créer des utilisateurs avec SQLModel.

        - create_one(session, **kwargs) -> User
        Retourne une utilisateur random

        - create_many(session, nb_users=5, **kwargs) -> List[User]
        Retourne une liste d'utilisateurs randoms
    """

    @classmethod
    def create_one(
            cls,
            session,
            id: Optional[int] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            email: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            roles: Optional[List[str]] = None,
            **kwargs,
    ) -> User:
        """Crée un seul utilisateur et l'ajoute à la session."""

        user = User(
            first_name=first_name or fake.first_name(),
            last_name=last_name or fake.last_name(),
            email=email or fake.email(),
            username=username or fake.user_name(),
            password=Auth.password_hash(password or fake.password()),
            is_active=True,
            roles=[]
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Ajout des rôles
        if roles:
            for role_enum in roles:
                role = RoleFactory.create_one(session=session, name=role_enum)
                user.roles.append(role)
            session.commit()
            session.refresh(user)

        return user

    @classmethod
    def create_many(cls, session, nb_users: int = 5, **kwargs) -> List:
        users = []
        for _ in range(nb_users):
            user = cls.create_one(session, **kwargs)
            users.append(user)
        return users
