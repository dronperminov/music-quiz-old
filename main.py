import os
from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn.config import LOGGING_CONFIG

from src.api.api import router as api_router
from src.api.audios import router as audios_router
from src.api.auth import router as auth_router
from src.api.settings import router as settings_router
from src.database import database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    database.connect()
    yield
    database.close()


app = FastAPI(lifespan=lifespan)


def main() -> None:
    app.include_router(api_router)
    app.include_router(auth_router)
    app.include_router(settings_router)
    app.include_router(audios_router)

    app.add_middleware(GZipMiddleware, minimum_size=500)

    StaticFiles.is_not_modified = lambda *args, **kwargs: False
    app.mount("/styles", StaticFiles(directory="web/styles"))
    app.mount("/js", StaticFiles(directory="web/js"))
    app.mount("/fonts", StaticFiles(directory="web/fonts"))
    app.mount("/images", StaticFiles(directory="web/images"))

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"

    host = os.getenv("MUSIC_QUIZ_HOST", "0.0.0.0")
    port = int(os.getenv("MUSIC_QUIZ_PORT", "6542"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
