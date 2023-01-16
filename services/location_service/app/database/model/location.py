from database.base import Base
from sqlalchemy_utils import UUIDType
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Float,
    String,
    Index,
    Boolean
)


class LocationModel(Base):
    __tablename__ = 'groups'
    __repr_attrs__ = ["id", "user_uuid", "name", "latitude", "longitude", "description", "has_image"]
    __table_args__ = (Index("idx_location_001", "user_uuid", "name", unique=True),)

    id = Column(Integer, Identity(), primary_key=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False, index=True)
    name = Column(String(50), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String(150), nullable=True)
    has_image = Column(Boolean, nullable=False)
