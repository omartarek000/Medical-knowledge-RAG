from fastapi import FastAPI
from src.app.routes import base , data



app = FastAPI()

app.include_router(base.api_router)
app.include_router(data.data_router)


