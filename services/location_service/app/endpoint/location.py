from database.base import get_db
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter


location_router = InferringRouter()


@cbv(location_router)
class LocationRouter:

    @location_router.post("/location", status_code=status.HTTP_201_CREATED)
    async def board_types_get_all(self, db: Session = Depends(get_db)):
        return await LocationBusiness(db).create()

    @s3_router.post("/{user_guid}/", status_code=HTTP_200_OK)
    async def post_bucket(self, image: UploadFile, path_name: str, user_guid: str) -> BucketIsSuccessSchema:
        return await S3().upload_file(image, user_guid, path_name)