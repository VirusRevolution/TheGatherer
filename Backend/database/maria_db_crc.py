import mariadb

from config.config import config
from database.api import DatabaseAPI


class MariaDB(DatabaseAPI):

    def __init__(self):
        """
        create connection to MariaDB, update tables if required
        """
        super().__init__()
        self.connection = mariadb.connect(
            host=config.db.host,
            user=config.db.user,
            password=config.db.password,
            database=config.db.database,
            port=config.db.port
        )
        self.update_tables()


    def update_tables(self):
        """
        create/update tables as required
        :return:
        """
        pass
