from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from database.base import get_db
from fastapi import Depends, status
from fastapi_utils.cbv import cbv
from business.device import BoardBusiness
from schema.board import BoardTypeListSchema, BoardTypeSchema

device_router = InferringRouter()


@cbv(device_router)
class BoardRouter:

    @device_router.get("/boardtypes")
    async def board_types_get_all(self, db: Session = Depends(get_db)) -> BoardTypeListSchema:
        return await BoardBusiness(db).board_type_get_all()

    @device_router.get("/boardtype/{board_type_id}")
    async def board_types_get(
            self,
            board_type_id: int,
            db: Session = Depends(get_db)) -> BoardTypeSchema:
        return await BoardBusiness(db).board_type_get(board_type_id)

    @device_router.put("/boardtype/{board_type_id}")
    async def board_type_update(
            self,
            board_type_id: int,
            board_type_body: BoardTypeSchema,
            db: Session = Depends(get_db),
    ) -> BoardTypeSchema:
        return await BoardBusiness(db).board_type_update(
            board_type_id=board_type_id,
            board_type_body=board_type_body
        )


@cbv(device_router)
class HealthRouter:

    @device_router.post("/health", status_code=status.HTTP_200_OK)
    async def health(self):
        return {"status": "ok"}
