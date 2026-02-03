from typing import Optional
from sqlmodel import SQLModel, Field


class UpdateUpdate(SQLModel):
    update_type: Optional[str] = Field(default=None, max_length=30)