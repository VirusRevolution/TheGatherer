import uvicorn
from api.api                 import API
from config.config           import config
from logging                 import DEBUG, getLogger
from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles     import StaticFiles
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
    app.include_router(API(), prefix="/api")
    app.mount("/", StaticFiles(directory="../Frontend/dist", html=True), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    LOG.info("Starting webserver…")

    uvicorn.run(app, **options)