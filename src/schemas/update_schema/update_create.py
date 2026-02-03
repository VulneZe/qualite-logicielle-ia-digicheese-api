from sqlmodel import SQLModel, Field


class UpdateCreate(SQLModel):
    update_type: str = Field(max_length=30)