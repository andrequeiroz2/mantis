from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import status, UploadFile
from business.aws import AwsBusiness
from uuid import UUID

aws_router = InferringRouter()


@cbv(aws_router)
class AwsRouter:

    @aws_router.post("/internal/s3/image/location", status_code=status.HTTP_201_CREATED)
    async def s3_image_location_create(
            self,
            image_name: str,
            user_uuid: UUID,
            location_name: str,
            image: UploadFile
    ):

        return await AwsBusiness().s3_image_location_create(
            user_uuid=user_uuid,
            location_name=location_name,
            image_name=image_name,
            image=image
        )
