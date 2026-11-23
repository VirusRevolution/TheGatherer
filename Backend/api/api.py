import uuid

from config.config     import config
from constants.misc import GET, POST
from fastapi           import APIRouter, Header
from logging           import getLogger


LOG = getLogger("api")

class API(APIRouter):
    def __init__(self):
        super().__init__()
        LOG.info("attaching /api/hello …")
        self.add_api_route(path="/hello", endpoint=self._hello, methods=[GET], tags=["API", "hello world"])

    def _hello(self):
        return {"message": "Hello World!"}

