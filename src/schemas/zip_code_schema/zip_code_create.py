from sqlmodel import SQLModel, Field

class ZipCodeCreate(SQLModel):
    code: str = Field(nullable=False, min_length=5, max_length=5)
    department_id: int = Field(nullable=False)