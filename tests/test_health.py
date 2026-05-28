#What this code does ?
#Is FastAPI application alive and responding correctly?


from fastapi.testclient import TestClient
from src.api.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}