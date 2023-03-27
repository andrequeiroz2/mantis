from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database.model.location import LocationModel
from schema.location import LocationSchema, LocationsSchema, LocationFilterSchema, LocationPutSchema
from schema.user import UserEmailFilterSchema
from pydantic import EmailStr
from uuid import UUID

class LocationBusiness:

    def __init__(self, db: Session):
        self.db = db

    async def post_location(
            self,
            location_schema: LocationSchema,
    ):
        location = self.get_location(location_schema)

        if location:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Location name already exists",
            )

        try:
            new_location = LocationModel(
                user_email=location_schema.user_email,
                location_name=location_schema.location_name,
                latitude=location_schema.latitude,
                longitude=location_schema.longitude,
                description=location_schema.description
            )
            self.db.add(new_location)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Location server error",
            )

        return new_location

    async def get_locations(self, user_email_filter_schema: UserEmailFilterSchema) -> [LocationsSchema]:
        location_list_model = []
        for location_model in self.db.query(LocationModel).filter_by(user_email=user_email_filter_schema.user_email).all():
            location_list_model.append(
                LocationsSchema(
                    location_uuid=location_model.location_uuid,
                    user_email=location_model.user_email,
                    location_name=location_model.location_name,
                    latitude=location_model.latitude,
                    longitude=location_model.longitude,
                    description=location_model.description,
                )
            )
        return location_list_model

    def get_location(self, location_filter_schema: LocationSchema):
        try:
            return self.db.query(LocationModel).filter_by(
                user_email=location_filter_schema.user_email,
                location_name=location_filter_schema.location_name
                ).first()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="location server error",
            )

    async def get_location_filter_email_uuid(self, location_filter_schema: LocationFilterSchema):
        try:
            location_model: LocationModel = self.db.query(LocationModel).filter_by(
                user_email=location_filter_schema.user_email,
                location_uuid=location_filter_schema.location_uuid
            ).first()

            return location_model

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="location server error",
            )

    async def put_location(
            self,
            user_email: EmailStr,
            location_uuid: UUID,
            location_schema: LocationPutSchema):

        location_model_check = self.check_location_exists(
            user_email=user_email,
            location_name=location_schema.location_name,
            location_uuid=location_uuid
        )

        if location_model_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Location name already exists",
            )

        location_model: LocationModel = self.db.query(LocationModel).filter_by(
            user_email=user_email,
            location_uuid=location_uuid
        ).update({
            "location_name": location_schema.location_name,
            "latitude": location_schema.latitude,
            "longitude": location_schema.longitude,
            "description": location_schema.description
        })

        return location_model

    def check_location_exists(self, user_email: EmailStr, location_name: str, location_uuid: UUID):
        return self.db.query(LocationModel).filter(
            LocationModel.user_email == user_email,
            LocationModel.location_name == location_name,
            LocationModel.location_uuid != location_uuid
        ).first()

