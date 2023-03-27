from database.base import get_db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from business.location import LocationBusiness
from schema.location import LocationSchema, LocationFilterSchema, LocationPutSchema
from schema.user import UserEmailFilterSchema
from pydantic import EmailStr
from uuid import UUID

location_router = InferringRouter()


@cbv(location_router)
class LocationRouter:

    @location_router.post("/location", status_code=status.HTTP_201_CREATED)
    async def location_create(
            self,
            location_schema: LocationSchema,
            db: Session = Depends(get_db)
    ):
        return await LocationBusiness(db).post_location(location_schema)

    @location_router.get("/location")
    async def location_get_filter(
            self,
            location_filter_schema: LocationFilterSchema = Depends(),
            db: Session = Depends(get_db)
    ):
        return await LocationBusiness(db).get_location_filter_email_uuid(location_filter_schema)

    @location_router.get("/locations")
    async def location_get_all(
            self,
            user_email_filter_schema: UserEmailFilterSchema = Depends(),
            db: Session = Depends(get_db)
    ):
        return await LocationBusiness(db).get_locations(
            user_email_filter_schema,
        )

    @location_router.put("/location/{user_email}/{location_uuid}")
    async def location_update(
            self,
            user_email: EmailStr,
            location_uuid: UUID,
            location_schema: LocationPutSchema,
            db: Session = Depends(get_db)):
        return await LocationBusiness(db).put_location(
            user_email=user_email,
            location_uuid=location_uuid,
            location_schema=location_schema
        )

    @location_router.post("/health", status_code=status.HTTP_200_OK)
    async def health(self):
        return {"status": "ok"}
