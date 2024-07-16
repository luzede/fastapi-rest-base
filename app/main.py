# ENTRY POINT FOR THE APPLICATION

from fastapi import FastAPI
from app.example.router import router as example_router
from app.auth.router import router as auth_router
from app.models import Base  # noqa: F401


app = FastAPI()

app.include_router(auth_router)
app.include_router(example_router)
