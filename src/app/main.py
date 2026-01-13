from fastapi import FastAPI
from src.app.routes import base


app = FastAPI()

app.include_router(base.api_router)

