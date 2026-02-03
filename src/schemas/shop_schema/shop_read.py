from datetime import date as dt_date
from sqlmodel import SQLModel


class ShopRead(SQLModel):
    id: int
    item_id: int

    date: dt_date
    quantity_shop: int