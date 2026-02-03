from sqlmodel import SQLModel, Field

class AddressBase(SQLModel):
    address: str = Field(default=None, nullable=False)
    address_complement_first: str | None = Field(default=None, nullable=True)
    address_complement_second: str | None = Field(default=None, nullable=True)