from database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
)
from sqlalchemy_utils import UUIDType


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, Identity(), primary_key=True)
    useruid = Column(UUIDType(binary=False), nullable=False, index=True)
    username = Column(String(50), index=True, unique=True)
    email = Column(String(60), index=True)
    password = Column(String(120))
