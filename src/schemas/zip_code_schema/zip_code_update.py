from sqlmodel import SQLModel, Field

class ZipCodeUpdate(SQLModel):
    code: str | None = Field(default=None, nullable=False, min_length=5, max_length=5)
    department_id: int | None = None