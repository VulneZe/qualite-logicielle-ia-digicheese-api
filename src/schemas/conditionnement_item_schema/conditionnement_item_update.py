from typing import Optional
from sqlmodel import SQLModel, Field


class ConditionnementItemUpdate(SQLModel):
    quantity_min: Optional[int] = Field(default=None, ge=0)
    quantity_max: Optional[int] = Field(default=None, ge=0)