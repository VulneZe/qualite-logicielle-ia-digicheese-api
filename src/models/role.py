from sqlmodel import SQLModel,Field, Relationship
from .base.role_base import RoleBase
from .link import UserRoleLink


class Role(RoleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink,
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all"}
    )
