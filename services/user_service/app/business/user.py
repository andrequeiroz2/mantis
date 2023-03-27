from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from schema.token import TokenSchema
from schema.user import UserSchema, UserListSchema, UserUuidSchema, UserEmailFilter, \
    UserHasSchema
from database.model.user import UserModel
from dependency.oauth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token
import bcrypt
import re


class UserBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def user_get_all(self):
        """
        Lista todos os usuarios
        :return: lista de usuarios
        """
        user_list = []
        for user in self.db.query(UserModel).all():
            user_list.append(
                UserSchema(
                    username=user.username,
                    email=user.email
                )
            )
        return UserListSchema(users=user_list, total=self.db.query(UserModel).count())

    async def user_get(self, user_id: int) -> UserSchema:
        return self._user_filter_id(user_id)

    async def post_user(self, user_body: UserSchema) -> UserModel:
        """
        Cadastra um novo usuario
        :param user_body: schema do pydantic
        :return: model de usuario
        """
        self._user_body_check(user_body)
        user = self._user_filter_email(user_body.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "user already registered"},
                headers={"X-Error": "internal request error"}
            )
        new_user = UserModel(username=user_body.username, email=user_body.email)
        self.db.add(new_user)
        # self.db.commit()
        return new_user

    async def user_has(self, user_email_filter: UserEmailFilter) -> UserHasSchema:
        try:
            user = self._user_filter_email(user_email_filter.user_email)
            has_user = True
            if not user:
                has_user = False
            return UserHasSchema(check=has_user)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="user service unavailable",
                headers={"X-Error": "internal request error"}
            )

    async def user_login(self, email: str, password: str) -> TokenSchema:
        """
        Login de usuario
        :param email: user email
        :param password: user password
        :return: token jwt
        """
        login_exception = HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "email or password, incorrect"},
            headers={"X-Error": "body error"}
        )

        user = self._user_filter_email(email)

        if not user:
            raise login_exception

        if not self._password_hashed_check(password, user.password):
            raise login_exception

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"email": user.email, "user": user.username}, expires_delta=access_token_expires)

        return TokenSchema(token=access_token)

    async def decode_token(self, token: str):
        decode_access_token(token)


    @staticmethod
    def _password_hashed(password: str) -> str:
        """
        Gera um hash
        :param password: passorwd do usuario
        :return: password hash
        """
        pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return pwhash.decode('utf8')

    @staticmethod
    def _password_hashed_check(password: str, hash_pass: str) -> bool:
        """
        Verifica se o password e valido
        :param password: password do usuario
        :param hash_pass: password hash
        :return: boolean
        """
        return bcrypt.checkpw(password.encode('utf-8'), hash_pass.encode('utf-8'))

    def _user_filter_email(self, email: str):
        """
        Pesquisa usuario por email
        :param email: email do usuario
        :return: model de usuario
        """
        return self.db.query(UserModel).filter_by(email=email).first()

    def _user_filter_id(self, user_id: int) -> UserSchema:
        """
        Pesquisa usuario por id
        :param user_id: id do usuario
        :return: schema do pydantic
        """
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "User not found"},
                headers={"X-Error": "query error"}
            )
        return UserSchema( username=user.username, email=user.email)

    @staticmethod
    def _user_body_check(user_body: UserSchema):
        """
        Verifica se o json enviado atende as regras
        :param user_body: schema do pydantic
        :return: Nao retorna
        """
        error_field = False

        if len(user_body.username) > 50:
            error_field = True

        email = user_body.email.replace(" ", "")
        if len(email) > 60 or not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            error_field = True

        if error_field:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail={"error": "sytem error"},
            )

    ##INTERNAL REQUESTS
    async def user_internal_get(self, email: str) -> UserUuidSchema:
        user = self._user_filter_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "User not found"},
                headers={"X-Error": "path error"}
            )
        return UserUuidSchema(user_uuid=user.useruid)

    # def get_user(self, username: str):
    #     """
    #     Pesquisa usuario por username
    #     :param username: username do usuario
    #     :return: schema do pydantic
    #     """
    #     user = self.db.query(UserModel).filter_by(username=username).first()
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={"error": "User not found"},
    #             headers={"X-Error": "body error"}
    #         )
    #     return UserPassSchema(
    #         username=user.username,
    #         email=user.email,
    #         hashed_password=user.password)
