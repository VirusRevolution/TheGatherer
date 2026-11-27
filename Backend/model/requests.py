from pydantic import BaseModel

"""
we collect fastapi request types here
"""

class SessionRequest(BaseModel):
    email: str