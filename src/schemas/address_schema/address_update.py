from sqlmodel import SQLModel, Field

class AddressUpdate(SQLModel):
    address: str | None = Field(default=None, min_length=3)
    address_complement_first: str | None = Field(default=None, min_length=3)
    address_complement_second: str | None = Field(default=None, min_length=3)
    zip_code_id: int | None = Field(default=None)
    commune_id: int | None = Field(default=None)
