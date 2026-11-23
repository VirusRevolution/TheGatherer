from datetime import datetime
from pydantic import BaseModel

class OneTimePassword(BaseModel):
    token: str
    expires: datetime
    email : str

class User(BaseModel):
    email: str
    name: str
    projects: list[str]