import pymysql
from config.config    import config
from database.constants import *
from database.user_db import UserDB
from logging          import getLogger


LOG            = getLogger("MariaDB")
DB_VERSION     = "db_version"

class MariaDB(UserDB):

    def __init__(self):
        """
        create connection to MariaDB, update tables if required
        """
        super().__init__()
        self.connection = pymysql.connect(
            host=config.db.host,
            user=config.db.user,
            password=config.db.password,
            database=config.db.database,
            port=config.db.port
        )
        self._update_tables()
        LOG.info(f"Connected to database at {config.db.host}")

    def _create_institutions_table(self):
        with self.connection.cursor() as cursor:
            sql = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_INSTITUTIONS} (
                {ID}            INT PRIMARY KEY,
                {NAME}          VARCHAR(255) NOT NULL,
                {DEPARTMENT}    VARCHAR(255),
                {CREATION_TIME} TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );"""
            cursor.execute(sql)
            self.connection.commit()
        LOG.debug("Settings table created or already exists")

    def _create_settings_table(self):
        """
        The settings table is a key value store.
        Within this class we use it to keep track of the database version.
        :return:
        """
        sql = f"CREATE TABLE IF NOT EXISTS {TABLE_SETTINGS} (`key` VARCHAR(255) NOT NULL PRIMARY KEY, value TEXT)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()
        LOG.debug("Settings table created or already exists")

    def _create_user_table(self):
        with self.connection.cursor() as cursor:
            sql = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
                {USER_ID} VARCHAR(255) PRIMARY KEY,
                {NAME}    VARCHAR(255),
                {INSTITUTION}   INT REFERENCES {TABLE_INSTITUTIONS}({ID}) ON UPDATE CASCADE,
                {CREATION_TIME} TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
            cursor.execute(sql)
            self.connection.commit()
        LOG.debug("Settings table created or already exists")


    def _get_db_version(self) -> int:
        """
        Read last db version from settings table.
        If the table does not exist, return 0
        :return:
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT value FROM {TABLE_SETTINGS} WHERE `key` = '{DB_VERSION}'")
            result = cursor.fetchone()
            if result is None:
                return 0
        return int(result[0])

    def _update0(self) -> int:
        """
        this method is used to create the settings table
        :return: new value db_version
        """
        self._create_settings_table()
        return 1

    def _update1(self) -> int:
        """
        this method is used to create the settings table
        :return: new value db_version
        """
        self._create_institutions_table()
        self._create_user_table()
        return 2

    def _update_tables(self):
        """
        create/update tables as required
        :return:
        """
        db_version = self._get_db_version()
        if db_version == 0:
            db_version = self._update0()
        if db_version == 1:
            db_version = self._update1()
        # create/update tables here

        self._write_db_version(db_version)

    def _write_db_version(self, version: int) -> None:
        """
        write the latest db version back to the database
        :param version:
        :return:
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO {TABLE_SETTINGS} (`key`, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = VALUES(value)", (DB_VERSION, str(version)))
            self.connection.commit()
            LOG.debug(f"Database version set to {version}")