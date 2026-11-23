from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    projects: list[str]