import fastapi.testclient as testclient
from main import app

client = testclient.TestClient(app)

def test_welcome():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}