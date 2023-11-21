from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app
from .db_fixtures import session

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "url shortener"}


def test_create_url_key(session: Session):
    response = client.post("/url", json={"target_url": "https://apple.com"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["target_url"] == "https://apple.com"
    assert data["url"] is not None


def test_error_url_raises_error(session: Session):
    response = client.post("/url", json={"target_url": "notaurl"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Your provided URL is not valid"}


def test_existing_key_url_returns_result(session: Session):
    key = "EYJEA"
    response = client.get(f"/geturlfromkey/{key}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_"] == 1
    assert data["key"] == "EYJEA"
    assert data["target_url"] == "https://google.com"
