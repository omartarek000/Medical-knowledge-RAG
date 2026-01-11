import fastapi.testclient as testclient
from fastapi import FastAPI
from src.routes.base import api_router
import os 

app = FastAPI()
app.include_router(api_router)
client = testclient.TestClient(app)

def test_welcome():
    response = client.get("/RAG/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Welcome to the {os.getenv('APP_NAME', 'API')}  v{os.getenv('APP_VERSION', '1.0.0')}!"}