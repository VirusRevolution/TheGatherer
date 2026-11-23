from constants.misc    import GET
from database.api      import DatabaseAPI
from database.maria_db import MariaDB
from fastapi           import APIRouter
from logging           import getLogger


LOG = getLogger("api")

class API(APIRouter):
    def __init__(self):
        super().__init__()
        LOG.info("attaching /hello to /api…")
        self.add_api_route(path="/hello", endpoint=self._hello, methods=[GET], tags=["API", "hello world"])
        self.db : DatabaseAPI = MariaDB() # MariaDB implements DatabaseAPI

    def _hello(self):
        return {"message": "Hello World!"}