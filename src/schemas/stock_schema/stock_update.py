from typing import Optional
from sqlmodel import SQLModel

class StockUpdate(SQLModel):
    designation: Optional[str] = None