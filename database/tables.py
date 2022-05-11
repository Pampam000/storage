from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String
)
from .database import Base


class Product(Base):
    __tablename__ = 'products'

    name = Column(String, primary_key=True, index=True)
    quan = Column(Integer)


class User(Base):
    __tablename__ = "users"

    login = Column(String, primary_key=True, index=True)
    is_seller = Column(Boolean)
    hashed_password = Column(String)
