from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from database.base import get_db
from fastapi import Depends, status
from fastapi_utils.cbv import cbv
from business.device import IconBusiness, LastWillBusiness, DeviceBusiness
from schema.icon import IconSchema
from schema.last_will import LastWillSchema, LastWillListSchema

device_router = InferringRouter()


@cbv(device_router)
class IconRouter:
    @device_router.post("/icon", status_code=status.HTTP_201_CREATED)
    async def icon_create(self, icon: IconSchema, db: Session = Depends(get_db)) -> IconSchema:
        return await IconBusiness(db).icon_create(icon)

    @device_router.get("/icon/{icon_id}")
    async def icon_get(self, icon_id: int, db: Session = Depends(get_db)) -> IconSchema:
        return await IconBusiness(db).icon_get(icon_id)

    @device_router.put("/icon/{icon_id}")
    async def icon_update(self, icon_id: int, icon: IconSchema, db: Session = Depends(get_db)) -> IconSchema:
        return await IconBusiness(db).icon_update(icon_id, icon)

    @device_router.delete("/icon/{icon_id}", status_code=status.HTTP_202_ACCEPTED)
    async def icon_delete(self, icon_id: int, db: Session = Depends(get_db)):
        await IconBusiness(db).icon_delete(icon_id)
        return {"msg": "successful"}


@cbv(device_router)
class LastWillRouter:

    @device_router.post("/lastwill", status_code=status.HTTP_201_CREATED)
    async def last_will_create(self, last_will_schema: LastWillSchema, db: Session = Depends(get_db)) -> LastWillSchema:
        return await LastWillBusiness(db).last_will_create(last_will_schema)

    @device_router.get("/lastwill/{last_will_id}")
    async def last_will_get(self, last_will_id: int, db: Session = Depends(get_db)) -> LastWillSchema:
        return await LastWillBusiness(db).last_will_get(last_will_id)

    @device_router.get("/lastwills")
    async def last_will_get_all(self, db: Session = Depends(get_db)) -> LastWillListSchema:
        return await LastWillBusiness(db).last_will_get_all()

    @device_router.put("/lastwill/{last_will_id}")
    async def last_will_update(
            self,
            last_will_id: int,
            last_will_schema: LastWillSchema,
            db: Session = Depends(get_db)
    ) -> LastWillSchema:
        return await LastWillBusiness(db).last_will_update(last_will_id, last_will_schema)

@cbv(device_router)
class DeviceRouter:
    @device_router.get("/type_devices")
    async def get_type_devices(self, db: Session = Depends(get_db)):
        return await DeviceBusiness(db).get_type_devices()

    @device_router.get("/type_sensors")
    async def get_type_sensors(self, db: Session = Depends(get_db)):
        return await DeviceBusiness(db).get_type_sensors()

@cbv(device_router)
class HealthRouter:

    @device_router.post("/health", status_code=status.HTTP_200_OK)
    async def health(self):
        return {"status": "ok"}
