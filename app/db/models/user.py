
import sqlalchemy as sa
from sqlalchemy import Boolean, Column, Integer, String

from app.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    isactive = Column(Boolean, default=True, server_default=sa.true())
