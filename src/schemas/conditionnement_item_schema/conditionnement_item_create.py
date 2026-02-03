from sqlmodel import SQLModel, Field


class ConditionnementItemCreate(SQLModel):
    conditionnement_id: int = Field(gt=0)
    item_id: int = Field(gt=0)
    quantity_min: int = Field(ge=0)
    quantity_max: int = Field(ge=0)