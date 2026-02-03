# Repository de base pour l'accès aux données (pattern Repository)
from abc import ABC
from typing import Generic, TypeVar, Type, Optional, Any, Dict, List
from sqlmodel import select, SQLModel, Session  # Session SQLModel pour BDD
from sqlalchemy import asc, desc  # Pour tri ASC/DESC

# Type générique pour les modèles SQLModel
T = TypeVar("T", bound=SQLModel)

class AbstractRepository(Generic[T], ABC):
    """Repository abstrait avec méthodes CRUD de base."""

    def __init__(self, session: Session, model: Type[T]):
        self.session = session  # Session de base de données
        self.model = model    # Modèle SQLModel à gérer

    def find(self, id: Any) -> Optional[T]:
        """Trouve une entité par son ID."""
        return self.session.get(self.model, id)

    def find_all(self) -> List[T]:
        """Retourne toutes les entités."""
        statement = select(self.model)
        return self.session.exec(statement).all()

    def find_one_by(self, criteria: Dict[str, Any]) -> Optional[T]:
        """Trouve une entité par des critères (ex: email='test@test.com')."""
        statement = select(self.model)

        # Ajoute chaque critère WHERE
        for field, value in criteria.items():
            statement = statement.where(
                getattr(self.model, field) == value
            )

        return self.session.exec(statement).first()

    def find_by(
            self,
            criteria: dict[str, Any],
            order_by: dict[str, str] | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ) -> list[T]:
        """Recherche avancée avec critères, tri, pagination."""
        statement = select(self.model)

        for field, value in criteria.items():
            column = getattr(self.model, field)

            # Gestion des opérateurs spéciaux
            if isinstance(value, dict):
                if "in" in value:
                    statement = statement.where(column.in_(value["in"]))
                else:
                    raise ValueError(f"Opérateur non supporté : {value}")
            else:
                statement = statement.where(column == value)

        # Tri
        if order_by:
            for field, direction in order_by.items():
                column = getattr(self.model, field)
                statement = statement.order_by(
                    asc(column) if direction.lower() == "asc" else desc(column)
                )

        # Limite / offset
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)

        return self.session.exec(statement).all()

    def save(self, entity: T) -> T:
        """Sauvegarde une entité (création ou mise à jour)."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)  # Rafraîchit avec les données BDD
        return entity

    def remove(self, entity: T) -> None:
        """Supprime une entité."""
        self.session.delete(entity)
        self.session.commit()

    def delete(self, entity_id: int) -> T:
        """Supprime une entité par ID."""
        entity = self.find(entity_id)
        if entity:
            self.remove(entity)
        return entity


class ServiceEntityRepository(AbstractRepository[T]):
    """Repository pour les services avec méthodes CRUD de base."""
    pass
