from logging import getLogger

from fastapi import APIRouter

from constants.misc import GET

LOG = getLogger("api")

class API(APIRouter):
    def __init__(self):
        super().__init__()
        LOG.info("attaching /hello to /api…")
        self.add_api_route(path="/hello", endpoint=self._hello, methods=[GET], tags=["API", "hello world"])

    def _hello(self):
        return {"message": "Hello World!"}