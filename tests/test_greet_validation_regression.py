import pytest
from fastapi.testclient import TestClient

from app import app


client = TestClient(app, raise_server_exceptions=False)


@pytest.mark.parametrize("payload", [{}, {"name": "   "}])
def test_missing_or_blank_name_returns_readable_422(payload):
    response = client.post("/api/greet", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "Запрос отклонён: поле name обязательно и должно быть непустой строкой"
    )
    assert "Traceback" not in response.text


def test_valid_name_is_trimmed_and_greeted():
    response = client.post("/api/greet", json={"name": "  Ada  "})

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Ada!"}
