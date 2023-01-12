from sqlalchemy.orm import Session
from database.model.device import BoardTypeModel
from schema.board import BoardTypeSchema, BoardTypeListSchema
from fastapi import HTTPException, status


class BoardBusiness:

    def __init__(self, db: Session):
        self.db = db

    async def board_type_get_all(self) -> BoardTypeListSchema:
        """
        Lista todos as boards
        :return: lista de boards
        """
        board_type_list = []
        for board in self.db.query(BoardTypeModel).all():
            board_type_list.append(
                BoardTypeSchema(
                    model=board.model,
                    version=board.version,
                    description=board.description
                )
            )
        return BoardTypeListSchema(boards_type=board_type_list, total=self.db.query(BoardTypeModel).count())

    async def board_type_get(self, board_type_id: int) -> BoardTypeSchema:
        board_type = self.db.query(BoardTypeModel).filter_by(id=board_type_id).first()
        if board_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "board type not found"},
                headers={"X-Error": "path error"}
            )

        return BoardTypeSchema(model=board_type.model, version=board_type.version, description=board_type.description)

    async def board_type_update(self, board_type_id: int, board_type_body: BoardTypeSchema) -> BoardTypeSchema:
        board_type = self.db.query(BoardTypeModel).filter_by(id=board_type_id).first()
        if board_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "board type not found"},
                headers={"X-Error": "path error"}
            )

        board_type.model = board_type_body.model
        board_type.version = board_type_body.version
        board_type.description = board_type_body.description

        self.db.add(board_type)

        return BoardTypeSchema(model=board_type.model, version=board_type.version, description=board_type.description)


