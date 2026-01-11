from fastapi import FastAPI
from dotenv import load_dotenv
from src.app.routes import base

load_dotenv()

app = FastAPI()

app.include_router(base.api_router)

