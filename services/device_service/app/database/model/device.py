from database.base import Base
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship, validates
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
    Index,
    ForeignKey,
    Boolean
)
import uuid



from database.mixin.mixin_util import TimestampMixin


class TypeDeviceModel(Base):
    __tablename__ = 'type_devices'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, unique=False)


class HubModel(Base, TimestampMixin):
    __tablename__ = 'hubs'
    __table_args__ = (
        Index("idx_hub_01", "name", "location_uuid", unique=True),
        Index("idx_hub_02", "user_email", "name", unique=True),
    )
    id = Column(Integer, Identity(), primary_key=True)
    user_email = Column(String(100), nullable=False, index=True)
    hub_uuid = Column(UUIDType(binary=False), nullable=False, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=False)
    description = Column(String(150))

    location_uuid = Column(UUIDType(binary=False), nullable=False, index=True)
    last_will_id = Column(Integer, ForeignKey("last_wills.id"), nullable=True)
    icons_id = Column(Integer, ForeignKey("icons.id"), nullable=False, index=True)


class SensorModel(Base, TimestampMixin):
    __tablename__ = 'sensors'
    __table_args__ = (
        Index("idx_sensors_01", "name", "location_uuid", unique=True),
        Index("idx_sensors_02", "name", "user_email", unique=True),
    )

    id = Column(Integer, Identity(), primary_key=True)
    user_email = Column(String(100), nullable=False, index=True)
    sensor_uuid = Column(UUIDType(binary=False), nullable=False, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=False, index=True)
    description = Column(String(150), nullable=True)
    location_uuid = Column(UUIDType(binary=False), nullable=False, index=True)
    hub_id = Column(Integer, ForeignKey("hubs.id"), nullable=True, index=True)
    last_will_id = Column(Integer, ForeignKey("last_wills.id"), nullable=True, index=True)
    type_sensor_id = Column(Integer, ForeignKey("type_sensors.id"), nullable=False, index=True)


class TypeSensorModel(Base):
    __tablename__ = 'type_sensors'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    max_scale = Column(Integer, nullable=True)
    min_scale = Column(Integer, nullable=True)
    measure_id = Column(Integer, ForeignKey("measures.id"), nullable=False, index=True)
    measure: "MeasureModel" = relationship("MeasureModel", innerjoin=True)


class MeasureModel(Base):
    __tablename__ = 'measures'
    __table_args__ = (
        Index("idx_measures_01", "name", "scale", unique=True),
    )
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False)
    scale = Column(String(3), nullable=False)
    icon_id = Column(Integer, ForeignKey("icon_sensors.id"), nullable=False, index=True)
    icon: "IconSensorModel" = relationship("IconSensorModel", innerjoin=True)


class IconSensorModel(Base):
    __tablename__ = 'icon_sensors'
    id = Column(Integer, Identity(), primary_key=True)
    font = Column(String(50), nullable=False)


class ActuatorModel(Base, TimestampMixin):
    __tablename__ = 'actuators'

    id = Column(Integer, Identity(), primary_key=True)
    actuator_uuid = Column(UUIDType(binary=False), nullable=False, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=False, index=True)
    description = Column(String(150), nullable=True)
    command_start = Column(String(50), nullable=True)
    command_stop = Column(String(50), nullable=True)
    command = Column(String(50), nullable=True)

    location_uuid = Column(UUIDType(binary=False), nullable=False, index=True)
    hub_id = Column(Integer, ForeignKey("hubs.id"), nullable=True, index=True)
    last_will_id = Column(Integer, ForeignKey("last_wills.id"), nullable=True)
    type_actuator_id = Column(Integer, ForeignKey("type_sensors.id"), nullable=False, index=True)


class TypeActuatorModel(Base):
    __tablename__ = 'type_actuators'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    icons_id = Column(Integer, ForeignKey("icons.id"), nullable=True, index=True)


class PublisherModel(Base, TimestampMixin):
    __tablename__ = 'publishers'
    id = Column(Integer, Identity(), primary_key=True)
    topic = Column(String(300), index=True, unique=True)
    qos_id = Column(Integer, ForeignKey("qos.id"), nullable=False, default=1)
    retain = Column(Boolean, nullable=False, default=True)
    actuator_id = Column(Integer, ForeignKey("actuators.id"), nullable=False, index=True)


class SubscriberModel(Base, TimestampMixin):
    __tablename__ = 'subscribers'
    id = Column(Integer, Identity(), primary_key=True)
    topic = Column(String(300), index=True, unique=True)
    qos_id = Column(Integer, ForeignKey("qos.id"), nullable=False, default=1)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False, index=True)


class LastWillModel(Base):
    __tablename__ = 'last_wills'

    id = Column(Integer, Identity(), primary_key=True)
    topic = Column(String(300), index=True, unique=True)


class QosModel(Base):
    __tablename__ = 'qos'

    id = Column(Integer, Identity(), primary_key=True)
    qos = Column(Integer, nullable=False, unique=True)

    @validates('qos')
    def validate_qos(self, key, value):
        if value not in (0, 1, 2):
            raise ValueError('qos invalid value. Valid values are: 0, 1, 2')
        return value


class IconModel(Base):
    __tablename__ = 'icons'

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    icon = Column(String(50), nullable=False, unique=True)
