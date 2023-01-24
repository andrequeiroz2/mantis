from fastapi import UploadFile, HTTPException, status
from uuid import UUID
from core.config import s3_client, settings
from botocore.errorfactory import ClientError
from botocore.exceptions import ParamValidationError


class AwsBusiness:

    async def s3_image_location_create(
        self,
        user_uuid: UUID,
        location_name: str,
        image: UploadFile
    ):

        try:
            s3_client.upload_fileobj(
                image.file,
                settings.S3_AWS_BUCKET_NAME,
                f"{settings.S3_AWS_BUCKET_PATH}/{user_uuid}/{location_name}/{image.filename}")
        except (ClientError, ParamValidationError) as err:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=err,
                headers={"X-Error": "dependency error"}
            )
