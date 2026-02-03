from sqlmodel import SQLModel

class LoginSchema(SQLModel):
    username: str
    password: str