import uvicorn
from logging import DEBUG, getLogger
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from config.config import config
from utils.logging_extension import add_logging_level, setup_logging

LOG = getLogger("server")

if __name__ == "__main__":
    add_logging_level('TRACE', DEBUG-5)
    setup_logging()

    options = {
        "host": config.web.bind_address,
        "port": config.web.port,
#        "reload": True,
        "log_level": "info",
        "log_config": None
    }

    app = FastAPI()
    app.mount("/", StaticFiles(directory="../Frontend", html=True), name="static")
    LOG.info("Starting webserver…")

    uvicorn.run(app, **options)