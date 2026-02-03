from sqlmodel import SQLModel


class ConditionnementItemRead(SQLModel):
    conditionnement_id: int
    item_id: int
    quantity_min: int
    quantity_max: int