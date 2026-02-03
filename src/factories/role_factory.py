from typing import List

import factory
from src.models.role import Role
from .interfaces.factories_interface import FactoriesInterface
from ..enum import RoleEnum

class RoleFactory(FactoriesInterface[Role]):
    """Factory “manuelle” pour SQLModel + pytest."""

    @staticmethod
    def create_one(session, name: RoleEnum):
        role = Role(name=name)
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

    @classmethod
    def create_many(cls, session, nb_roles: int = max(1, 5), **kwargs) -> List:
        roles = []
        for _ in range(nb_roles):
            role = cls.create_one(session, **kwargs)
            roles.append(role)
        return roles