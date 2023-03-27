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
import uuid

class LocationModel(Base):
    __tablename__ = 'locations'
    __repr_attrs__ = [
        "id", "user_email", "location_uuid", "location_name", "latitude",
        "longitude", "has_image", "description"
    ]
    __table_args__ = (
        Index("idx_location_001", "user_email", "location_name", unique=True),
    )

    id = Column(Integer, Identity(), primary_key=True)
    user_email = Column(String(100), nullable=False, index=True)
    location_uuid = Column(UUIDType(binary=False), nullable=False, index=True, default=uuid.uuid4)
    location_name = Column(String(20), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    has_image = Column(Boolean, nullable=False, default=False)
    description = Column(String(150), nullable=True)

