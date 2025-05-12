# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import router as api_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}", "debug": settings.DEBUG}
