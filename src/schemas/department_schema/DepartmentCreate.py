from sqlmodel import SQLModel, Field

class DepartmentCreate(SQLModel):
    number: str = Field(nullable=False, min_length=2, max_length=3)
