from sqlmodel import SQLModel, Field

class ZipCodeBase(SQLModel):
    code: str = Field(nullable=False, min_length=5, max_length=5, index=True, unique=True)


