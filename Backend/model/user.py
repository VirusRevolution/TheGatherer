from datetime import datetime, timedelta
from pydantic import BaseModel

SESSION_DURATION = timedelta(minutes=30) # todo: make configurable

class OneTimePassword(BaseModel):
    token: str
    expires: datetime
    email : str

class User(BaseModel):
    email: str
    name: str
    projects: list[str]
    is_admin: bool

class SessionData(BaseModel):
    expiration : datetime = datetime.now() + SESSION_DURATION
    user: User

    def extend(self):
        self.expiration = datetime.now() + SESSION_DURATION
        return self