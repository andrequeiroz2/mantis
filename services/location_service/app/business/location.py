import json
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
import requests
from database.model.location import LocationModel


class LocationBusiness:

    def __init__(self, db: Session):
        self.db = db

    async def post_location(
            self,
            user_email: str,
            location_name: str,
            image: UploadFile,
            location_latitude: float,
            location_longitude: float,
            location_description: str
    ):
        if image:
            has_image = True
        else:
            has_image = False

        try:
            request_user = requests.get(
                'http://localhost:8010/api/userservice/internal/user',
                params={'user_email': user_email}
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="user service unavailable",
                headers={"X-Error": "internal request error"}
            )

        if request_user.status_code != 200:
            detail = json.loads(request_user.text)['detail']
            raise HTTPException(
                status_code=request_user.status_code,
                detail=detail,
                headers={"X-Error": "internal request error"}
            )

        user_uuid = json.loads(request_user.text)['user_uuid']

        if has_image:

            files = {
                'image': image.file,
            }

            params = {
                'user_uuid': user_uuid,
                'image_name': image_name,
                'location_name': location_name
            }

            try:
                request_s3 = requests.post(
                    'http://localhost:8040/api/awsservice/internal/s3/image/location',
                    files=files,
                    params=params

                )
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="bucket service unavailable",
                    headers={"X-Error": "internal request error"}
                )

            if request_s3.status_code != 201:
                raise HTTPException(
                    status_code=request_s3.status_code,
                    detail=request_s3.text,
                    headers={"X-Error": "internal request error"}
                )

        try:
            new_location = LocationModel(
                user_uuid=user_uuid,
                has_image=has_image,
                location_name=location_name,
                latitude=location_latitude,
                longitude=location_longitude,
                description=location_description
            )
            self.db.add(new_location)
            self.db.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="location already exists",
                headers={"X-Error": "violates unique constraint"}
            )

        return new_location
