from sqlmodel import SQLModel, Field

class DepartmentBase(SQLModel):
    number: str = Field(nullable=False, min_length=2, max_length=3, index=True, unique=True)