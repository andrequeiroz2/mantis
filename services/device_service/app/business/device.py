from sqlalchemy.orm import Session
from database.model.device import IconModel, LastWillModel, TypeDeviceModel, TypeSensorModel
from schema.device import TypeDeviceList, TypeSensorListSchema
from schema.icon import IconSchema
from schema.last_will import LastWillSchema, LastWillListSchema
from fastapi import HTTPException, status


class LastWillBusiness:

    def __init__(self, db: Session):
        self.db = db

    async def last_will_create(self, last_will: LastWillSchema) -> LastWillSchema:
        last_will_dict = last_will.dict()
        new_last_will = LastWillModel(**last_will_dict)
        self.db.add(new_last_will)
        return LastWillSchema(topic=last_will.topic)

    async def last_will_get(self, last_will_id: int) -> LastWillSchema:
        last_will = self._last_will_filter_id(last_will_id)
        return LastWillSchema(topic=last_will.topic)

    async def last_will_get_all(self) -> LastWillListSchema:
        last_wills = self.db.query(LastWillModel).all()
        return LastWillListSchema(
            last_wills=last_wills,
            count=self.db.query(LastWillModel).count()
        )

    async def last_will_update(self, last_will_id: int, last_will_schema: LastWillSchema) -> LastWillSchema:
        last_will = self._last_will_filter_id(last_will_id)
        last_will.topic = last_will_schema.topic
        self.db.add(last_will)
        return LastWillSchema(topic=last_will_schema.topic)

    async def last_will_delete(self, last_will_id: int) -> None:
        _ = self._last_will_filter_id(last_will_id)
        self.db.query(LastWillModel).filter_by(id=last_will_id).delete()

    def _last_will_filter_id(self, last_will_id: int) -> LastWillModel:
        last_will = self.db.query(LastWillModel).filter_by(id=last_will_id).first()
        if not last_will:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Last Will not found"},
                headers={"X-Error": "query error"}
            )
        return last_will




class IconBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def icon_create(self, icon: IconSchema) -> IconSchema:
        icon_dict = icon.dict(exclude_none=True)
        new_icon = IconModel(**icon_dict)
        self.db.add(new_icon)
        return IconSchema(name=icon.name, icon=icon.icon)

    async def icon_get(self, icon_id: int) -> IconSchema:
        icon = self._icon_filter_id(icon_id)
        return IconSchema(name=icon.name, icon=icon.icon)

    async def icon_update(self, icon_id: int, icon: IconSchema) -> IconSchema:
        icon_mod = self._icon_filter_id(icon_id)
        icon_mod.name = icon.name
        icon_mod.icon = icon.icon
        self.db.add(icon_mod)
        return IconSchema(name=icon.name, icon=icon.icon)

    async def icon_delete(self, icon_id: int) -> None:
        _ = self._icon_filter_id(icon_id)
        self.db.query(IconModel).filter_by(id=icon_id).delete()

    def _icon_filter_id(self, icon_id: int) -> IconSchema:

        icon = self.db.query(IconModel).filter_by(id=icon_id).first()
        if not icon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Icon not found"},
                headers={"X-Error": "query error"}
            )
        return icon




class DeviceBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def get_type_devices(self) -> [TypeDeviceModel]:
        type_device_list = []
        for type_device_model in self.db.query(TypeDeviceModel).all():
            type_device_list.append(type_device_model)
        return type_device_list

    async def get_type_sensors(self) -> [TypeSensorListSchema]:
        type_sensor_list = []
        for type_sensor_model in self.db.query(TypeSensorModel).all():
            type_sensor_list.append(
                TypeSensorListSchema(
                    id=type_sensor_model.id,
                    name=type_sensor_model.name,
                    measure=type_sensor_model.measure.name,
                    scale=type_sensor_model.measure.scale,
                    max_scale=type_sensor_model.max_scale,
                    min_scale=type_sensor_model.min_scale,
                    icon=type_sensor_model.measure.icon.font
                )
            )
        return type_sensor_list
