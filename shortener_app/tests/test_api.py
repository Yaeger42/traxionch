from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from ..main import app, get_db
from ..database import Base
from ..models import URL
from ..crud import get_db_url_by_key, create_db_url
from ..schemas import URLBase
from typing import Generator
import pytest

client = TestClient(app)
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    url_item = URL(
        id_=1, target_url="https://google.com", is_active=True, clicks=0, key="EYJEA"
    )
    db_session.add(url_item)
    db_session.commit()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


def teardown():
    Base.metadata.drop_all(bind=engine)


def overrride_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overrride_get_db


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


def test_create_db_url(session: Session):
    url_base = URLBase(target_url="https://example.com")
    db_url = create_db_url(session, url_base)
    assert db_url.id_ is not None
    assert db_url.clicks == 0
    assert db_url.is_active == True
    assert db_url.key is not None


def test_get_url_by_key(session: Session):
    item = get_db_url_by_key(session, "EYJEA")
    assert item.key == "EYJEA"
