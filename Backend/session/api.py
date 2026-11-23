import uuid

from config.config     import config
from constants.misc import GET, POST, COOKIE_KEY
from fastapi import APIRouter, Header, Depends, Request, HTTPException, Response
from logging           import getLogger

from database import user_db
from database.user_db import UserDB
from message.messages import send_email
from model.requests import SessionRequest
from model.user import User, SessionData

LOG = getLogger("api")



class SessionAPI(APIRouter):
    def __init__(self, user_db : UserDB):
        super().__init__()
        self.add_api_route(path="/token", endpoint=self._token, methods=[POST], tags=["API", "SESSION"])
        self.add_api_route(path="/validate", endpoint=self._validate_otp, methods=[GET], tags=["API", "SESSION"])
        self.add_api_route(path="/user", endpoint=self._get_user, methods=[GET], tags=["API", "SESSION"])
        self.user_db = user_db
        LOG.info("attaching /api/session/get and /api/session/token")



    def _get_user(self, request: Request, response: Response):
        """
        Get user`s data (if there is a session a.k.a. valid session cookie).
        """
        session_data = self.session_cookie(request, response)
        return session_data


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

    def drop_cookie(self, response: Response, session_id: str):
        response.set_cookie(key=COOKIE_KEY,value=session_id,expires=-10)
        LOG.info('dropped cookie for session %s', session_id)

    def session_cookie(self, request: Request, response: Response) -> SessionData:
        session_id = request.cookies.get(COOKIE_KEY)
        if session_id is None:
            LOG.debug('request does not contain session_id')
            raise HTTPException(status_code=401,detail="no session_id")
        LOG.debug('checking session %s', session_id)
        session = self.user_db.get_session(session_id)

        if session is None:
            LOG.debug('no session data assigned with %s', session_id)
            self.drop_cookie(response, session_id)
            raise HTTPException(status_code=401,detail='session {0} is invalid'.format(session_id))

        return session