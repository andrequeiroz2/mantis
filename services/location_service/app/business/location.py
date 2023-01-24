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
            image_name: str,
            location_name: str,
            image: UploadFile,
            location_latitude: float,
            location_longitude: float,
            location_description: str
    ):

        request_user = requests.get(
            'http://localhost:8010/api/userservice/internal/user',
            params={'user_email': user_email}
        )

        if request_user.status_code != 200:
            detail = json.loads(request_user.text)['detail']

            raise HTTPException(
                status_code=request_user.status_code,
                detail=detail,
                headers={"X-Error": "internal request error"}
            )

        user_uuid = json.loads(request_user.text)['user_uuid']
        has_image = False

        if image:

            has_image = True

            files = {
                'image': image.file,
            }

            params = {
                'user_uuid': user_uuid,
                'image_name': image_name,
                'location_name': location_name
            }

            request_s3 = requests.post(
                'http://localhost:8040/api/awsservice/internal/s3/image/location',
                files=files,
                params=params

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
                image_name=image_name,
                has_image=has_image,
                location_name=location_name,
                latitude=location_latitude,
                longitude=location_longitude,
                description=location_description
            )
            self.db.add(new_location)
            self.db.commit()
            return new_location

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="location already exists",
                headers={"X-Error": "violates unique constraint"}
            )


    # def _internal_request(self, method:str, path:str, obj:Any):
    #     try:
    #
    #         if method == 'post':
    #             resp = requests.post(path, obj)
    #         elif method == 'get':
    #             resp = requests.get(path, obj)
    #         else:
    #             raise HTTPException(
    #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 detail={"error": "method not Allowed"},
    #                 headers={"X-Error": "internal request error"}
    #             )
    #         return resp
    #
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail={"error": f"internal connection {e}"},
    #             headers={"X-Error": "internal request error"}
    #         )
