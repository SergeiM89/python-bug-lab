from fastapi.testclient import TestClient
from app import app

client = TestClient(app, raise_server_exceptions=False)


def test_health():
    assert client.get("/health").status_code == 200


def test_correct_name():
    response = client.post("/api/greet", json={"name": "Ada"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Ada!"}


def test_missing_name_is_validation_error():
    assert client.post("/api/greet", json={}).status_code in {400, 422}
