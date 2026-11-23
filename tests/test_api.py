from app import app
from fastapi.testclient import TestClient

client = TestClient(app, raise_server_exceptions=False)


def test_health():
    assert client.get("/health").status_code == 200


def test_correct_name():
    response = client.post("/api/greet", json={"name": "Ada"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Ada!"}


def test_missing_name_is_validation_error():
    response = client.post("/api/greet", json={})
    assert response.status_code == 422
    assert response.json()["detail"]
    assert "Traceback" not in response.text


def test_empty_name_is_validation_error():
    response = client.post("/api/greet", json={"name": "   "})
    assert response.status_code == 422
    assert response.json()["detail"]


def test_error_diagnostics_are_visible_on_the_page():
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="result-status"' in response.text
    assert 'aria-label="Ответ и traceback backend"' in response.text
