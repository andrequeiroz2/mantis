from database.base import get_db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from fastapi import Depends, status, UploadFile, File, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from business.location import LocationBusiness


location_router = InferringRouter()


@cbv(location_router)
class LocationRouter:

    @location_router.post("/location", status_code=status.HTTP_201_CREATED)
    async def board_types_get_all(
            self,
            user_email: str,
            location_name: str,
            latitude: float,
            longitude: float,
            description: str,
            image: UploadFile = None,
            db: Session = Depends(get_db)
    ):

        if image:

            image_type = image.headers['content-type']

            if image_type != 'image/png' and image_type != 'image/jpg' and image_type != 'image/jpeg':
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="image with invalid extension. Use extensions: png, jpg, jpeg",
                    headers={"X-Error": "multipart error"}
                )

            # byte_image = await image.read()
            #
            # if len(byte_image) > 1048576:
            #     raise HTTPException(
            #         status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            #         detail="image larger than 1MB",
            #         headers={"X-Error": "multipart error"}
            #     )

        await LocationBusiness(db).post_location(
            user_email=user_email,
            image=image,
            location_name=location_name,
            location_latitude=latitude,
            location_longitude=longitude,
            location_description=description
        )

        return {"mgs": "success"}

    @location_router.post("/health", status_code=status.HTTP_200_OK)
    async def health(self):
        return {"status": "ok"}
