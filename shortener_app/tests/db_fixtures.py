import pytest
from sqlalchemy import create_engine, StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from ..main import app, get_db
from ..database import Base
from ..models import URL

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
