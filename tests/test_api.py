import fastapi.testclient as testclient
from fastapi import FastAPI
from src.app.routes.base import api_router
from src.app.routes.data import data_router
from src.app.helpers.config import get_settings , Settings
from src.app.Controllers import ProjectController

app = FastAPI()
app.include_router(api_router)
app.include_router(data_router)
client = testclient.TestClient(app)
app_settings = get_settings()

def test_welcome():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {"message": f"Welcome to the {app_settings.APP_NAME}  v{app_settings.APP_VERSION}!"}


def test_upload_data():
    project_id = "test_project"
    file_payload = {"file": ("test.txt" , b"Sample file content" , "text/plain")}

    response = client.post(f"/api/data/upload/{project_id}" , files=file_payload)
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}


def test_upload_data_invalid_file():
    project_id = "test_project"
    file_payload = {"file": ("test.exe" , b"Sample file content" , "application/octet-stream")}

    response = client.post(f"/api/data/upload/{project_id}" , files=file_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "File type is not allowed."}