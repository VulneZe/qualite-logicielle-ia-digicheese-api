from sqlmodel import SQLModel


class UpdateItemRead(SQLModel):
    update_id: int
    item_id: int
    quantity_update: int