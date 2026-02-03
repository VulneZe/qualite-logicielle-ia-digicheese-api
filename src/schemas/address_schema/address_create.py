from sqlmodel import SQLModel, Field

class AddressCreate(SQLModel):
    address: str = Field(default=None, nullable=False)
    address_complement_first: str | None = None
    address_complement_second: str | None = None
    zip_code_id: int = Field(nullable=False)
    commune_id: int = Field(nullable=False)

