from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from dependency.oauth import oauth2_scheme
from schema.token import TokenSchema
from schema.user import UserSchema, UserCreateSchema, UserListSchema
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.base import get_db
from business.user import UserBusiness
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


user_router = InferringRouter()


@user_router.get("/users")
async def user_get_all(_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserListSchema:
    return await UserBusiness(db).user_get_all()


@user_router.post("/user", status_code=status.HTTP_201_CREATED)
async def user_create(user_body: UserCreateSchema, db: Session = Depends(get_db)) -> UserSchema:
    user = await UserBusiness(db).post_user(user_body)
    return UserSchema(username=user.username, email=user.email)


@user_router.post("/user/login", response_model=TokenSchema)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await UserBusiness(db).user_login(form_data)


@user_router.post("/user/token/validate")
async def user_login(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    oi = await UserBusiness(db).decode_token(token)
    print(oi)
    return oi

