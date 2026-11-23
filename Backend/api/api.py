from constants.misc    import GET
from database.maria_db import MariaDB
from fastapi           import APIRouter
from logging           import getLogger

from database.user_db import UserDB

LOG = getLogger("api")

class API(APIRouter):
    def __init__(self):
        super().__init__()
        LOG.info("attaching /hello to /api…")
        self.add_api_route(path="/hello", endpoint=self._hello, methods=[GET], tags=["API", "hello world"])
        mariadb = MariaDB() # MariaDB implements DatabaseAPI
        self.user_db : UserDB = mariadb

    def _hello(self):
        return {"message": "Hello World!"}