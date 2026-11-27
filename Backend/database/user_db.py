from logging import getLogger

from model.user import User, OneTimePassword, SessionData


def not_implemented():
    raise RuntimeError("This method must be overwritten!")

class UserDB:
    """
	This class is an INTERFACE that abstracts methods required for user management.

	Methods we want to use in our application logic are defined here.
	The actual implementations are in the DB-specific implementations, e.g. mariadb.py
	"""

    def create_user(self, user: User):
        """
        create a new user in the database
        :param user:
        :return:
        """
        not_implemented()

    def get_user(self, email: str) -> User:
        """
        get a user out of the database
        :param email:
        :return:
        """
        not_implemented()

    def create_otp_for(self, email: str) -> str:
        """
        create a one-time password for the user, assign verfallsdatum
        :param email:
        :return:
        """
        not_implemented()

    def get_user_by_otp(self, otp: str) -> User | None:
        not_implemented()

    def get_session(self, session_id: str) -> SessionData | None:
        """
        if the session id is valid: load and return user
        otherwise: return None

        if session entry exists in database, but is expired: drop it
        :param session_id:
        :return:
        """
        not_implemented()

    def create_session_for(self, user: User) -> str:
        """
        create a session, return session id
        """
        not_implemented()

