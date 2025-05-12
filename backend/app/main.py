# app/main.py

from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)


@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "debug": settings.DEBUG
    }
