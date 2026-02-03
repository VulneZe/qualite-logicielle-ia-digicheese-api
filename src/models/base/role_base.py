from typing import List

from sqlmodel import SQLModel, Relationship, Field
from ...enum import RoleEnum


class RoleBase(SQLModel):
    name: RoleEnum = Field(nullable=False)


