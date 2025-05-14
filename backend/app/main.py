import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1.routes import router as api_router
from app.indexing.search_service import preload_index_and_metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    preload_index_and_metadata()
    yield


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}", "debug": settings.DEBUG}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    return {"status": "pong"}
