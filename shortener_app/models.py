from sqlalchemy import Boolean, Column, String, Integer

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id_ = Column(Integer, primary_key=True, name="id")
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
