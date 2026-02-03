from sqlmodel import SQLModel, Field

class PersonneBase(SQLModel):
    last_name: str = Field(nullable=False, min_length=2)
    first_name: str = Field(nullable=False, min_length=2)
