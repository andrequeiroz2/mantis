from fastapi import Depends, status, Header, Form
from fastapi_utils.inferring_router import InferringRouter
from schema.token import TokenSchema
from schema.user import UserSchema, UserCreateSchema, UserListSchema, UserUuidSchema
from sqlalchemy.orm import Session
from database.base import get_db
from business.user import UserBusiness


user_router = InferringRouter()


@user_router.get("/users")
async def user_get_all(db: Session = Depends(get_db)) -> UserListSchema:
    return await UserBusiness(db).user_get_all()


@user_router.get("/user/{user_id}")
async def user_get_all(user_id: int, db: Session = Depends(get_db)) -> UserSchema:
    return await UserBusiness(db).user_get(user_id)


@user_router.post("/user", status_code=status.HTTP_201_CREATED)
async def user_create(user_body: UserCreateSchema, db: Session = Depends(get_db)) -> UserSchema:
    user = await UserBusiness(db).post_user(user_body)
    return UserSchema(username=user.username, email=user.email)


@user_router.post("/user/login", response_model=TokenSchema)
async def user_login(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    return await UserBusiness(db).user_login(email, password)


@user_router.post("/auth", status_code=status.HTTP_200_OK)
async def access_validation(authorization: str = Header(None), db: Session = Depends(get_db)):
    await UserBusiness(db).decode_token(authorization)


@user_router.post("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}


##INTERNAL REQUESTS
@user_router.get("/internal/user")
async def user_internal_get(user_email: str, db: Session = Depends(get_db)) -> UserUuidSchema:
    return await UserBusiness(db).user_internal_get(user_email)
