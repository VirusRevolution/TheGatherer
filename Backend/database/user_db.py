from model.user import User


class UserDB:
    """
	This is just the interface

	Methods we want to use in our application logic are defined here.
	The actual implementations are in the DB-specific implementations, e.g. mariadb.py
	"""

    def create_user(self, user: User):
        """
        create a new user in the database
        :param user:
        :return:
        """

    def get_user(self, email: str) -> User:
        """
        get a user out of the database
        :param email:
        :return:
        """
        pass