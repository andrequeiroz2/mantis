from database.base import Base
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
    Index,
    ForeignKey
)

from database.mixin.mixin_util import TimestampMixin


class BoardTypeModel(Base, TimestampMixin):
    __tablename__ = 'board_types'
    __repr_attrs__ = ["id", "name", "model", "version", "description"]
    __table_args__ = (Index("idx_board_type_01", "model", "version", unique=True),)

    id = Column(Integer, Identity(), primary_key=True)
    model = Column(String(50), nullable=False, index=True)
    version = Column(String(10), nullable=False)
    description = Column(String(150))

    # controller = relationship("BoardModel", back_populates="board_types", innerjoin=True)


class BoardModel(Base, TimestampMixin):
    __tablename__ = 'boards'
    __repr_attrs__ = ["id", "name", "description", "board_types_id", "user_uuid", "location_uuid"]
    __table_args__ = (Index("idx_board_001", "name", "user_uuid", "location_uuid", unique=True),)

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(150))
    board_types_id = Column(Integer, ForeignKey("board_types.id"), nullable=False, index=True)
    user_uuid = Column(UUIDType(binary=False), nullable=False, index=True)
    location_uuid = Column(UUIDType(binary=False), nullable=False, index=True)

    # board_types = relationship("BoardTypeModel", back_populates="controller", innerjoin=True)
    shild = relationship("ShildModel", back_populates="board", innerjoin=True)


class ShildModel(Base, TimestampMixin):
    __tablename__ = 'shilds'
    __repr_attrs__ = [
        "id", "name", "model", "version", "description", "scale", "scale_max",
        "scale_min", "command_on", "command_off", "command_generic", "board_id"
    ]

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    model = Column(String(50), nullable=False)
    version = Column(String(10), nullable=False)
    description = Column(String(150))
    scale = Column(String(4))
    scale_max = Column(Integer)
    scale_min = Column(Integer)
    command_on = Column(String(120))
    command_off = Column(String(120))
    command_generic = Column(String(120))

    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)

    board = relationship("BoardModel", back_populates="shild", innerjoin=True)

#
# class ShildType(Base):
#     __tablename__ = 'shild_types'
#     id = Column(Integer, Identity(), primary_key=True)
#     model = Column(String(50), index=True)
#     version = Column(String(10))
#     description = Column(String(150))

# class TopicModel(Base):
#     __tablename__ = 'cliente_mqtts'
#     __repr_attrs__ = ["id", "topic", "topic_last_will", "message_last_will"]
#
#     id = Column(Integer, Identity(), primary_key=True)
#     topic = Column(String(300), index=True, unique=True)
#     topic_last_will = Column(String(300), index=True, unique=True)
#     message_last_will = Column(String(300))


