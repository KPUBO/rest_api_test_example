from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router
from core.config import settings
from core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("Session dispose")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan
)
main_app.include_router(router,
                        prefix=settings.api.prefix)
if __name__ == '__main__':
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
