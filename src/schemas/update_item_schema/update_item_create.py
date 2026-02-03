from sqlmodel import SQLModel, Field


class UpdateItemCreate(SQLModel):
    update_id: int
    item_id: int
    quantity_update: int = Field(ge=0)