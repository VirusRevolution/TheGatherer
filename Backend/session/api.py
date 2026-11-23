import uuid

from config.config     import config
from constants.misc import GET, POST
from fastapi           import APIRouter, Header
from logging           import getLogger

from database.user_db import UserDB
from message.messages import send_email
from model.requests import SessionRequest
from model.user import User

LOG = getLogger("api")

class SessionAPI(APIRouter):
    def __init__(self, user_db : UserDB):
        super().__init__()
        self.add_api_route(path="/token", endpoint=self._token, methods=[POST], tags=["API", "SESSION"])
        self.add_api_route(path="/validate", endpoint=self._validate_otp, methods=[GET], tags=["API", "SESSION"])
        self.user_db = user_db
        LOG.info("attaching /api/session/get and /api/session/token")

    def _token(self, req: SessionRequest) -> str:
        email = req.email
        # TODO: check if user is either in config.admin_users or in the user_db
        otp = self.user_db.create_otp_for(email)
        send_email(email,"Your login otp",f"Your login otp is {otp}. Go to {config.web.base_url}/login?otp={otp} to login.")
        # TODO: return response

    def _validate_otp(self, otp : str = Header(None)):
        user = self.user_db.get_user_by_otp(otp)
        if user is None:
            pass # TODO: return error
        session_id = self.user_db.create_session_for(user)
        # return session id to frontend, frontend must then set cookie with session_id

    def get_user_by_session_id(self, session_id: str) -> User|None:
        """
        This will later be used to assign requests to users
        """
        return self.user_db.get_user_by_session_id(session_id)