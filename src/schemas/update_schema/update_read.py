from datetime import datetime
from sqlmodel import SQLModel


class UpdateRead(SQLModel):
    id: int
    update_type: str
    update_date: datetime