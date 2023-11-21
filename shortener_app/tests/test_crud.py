from ..crud import get_db_url_by_key, create_db_url
from ..schemas import URLBase
from sqlalchemy.orm import Session
from .db_fixtures import session


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
