from typing import Optional
from sqlmodel import SQLModel, Field


class UpdateItemUpdate(SQLModel):
    quantity_update: Optional[int] = Field(default=None, ge=0)