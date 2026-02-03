from sqlmodel import SQLModel, Field, Relationship
from .base.user_base import UserBase
from .link import UserRoleLink


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(nullable=False, min_length=12)
    roles: list["Role"] = Relationship(
        back_populates="users",
        link_model=UserRoleLink,
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all"
        }
    )
