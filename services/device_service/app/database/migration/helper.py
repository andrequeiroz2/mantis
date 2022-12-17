from sqlalchemy import text
from sqlalchemy.engine import Connection
from core.config import settings


class DBSchemaMigrate:

    def __init__(self, connection: Connection):
        self.connection = connection
        self.schema = settings.DBBASE
        self.user_name = settings.DBUSER
        self.password = settings.DBPASSWORD

    def create_user(self, user_name: str, password: str):
        """
        Cria o usuário caso ele nao exista.
        :param user_name: nome do usuário do banco
        :param password: senha do usuário do banco
        :return: N/A
        """
        if self.check_user_exist(user_name):
            return

        try:
            self.connection.execute(
                text(
                    f"CREATE USER {user_name} WITH LOGIN NOCREATEDB CREATEROLE INHERIT ENCRYPTED PASSWORD :password;"
                ).bindparams(password=password)
            )
        except:
            print("error: check the function create_user()")

    def check_user_exist(self, user_name: str) -> bool:
        """
        Verifica se o usuário ja existe no DB.
        :param user_name: nome do usuário.
        :return Booleano indicando se existe ou nao
        """
        try:
            return (
                self.connection.execute(
                    text("SELECT usename FROM pg_user WHERE  usename = :user_name").bindparams(user_name=user_name)
                ).first()
                is not None
            )
        except:
            print("error: check the function check_user_exist()")

    def install_db_extensions(self):
        """Instala as extensoes do banco"""
        try:
            _ = [
                self.connection.execute(text(f"CREATE EXTENSION IF NOT EXISTS {extension_name} WITH SCHEMA {self.schema};"))
                for extension_name in ("uuid-ossp",)
            ]
        except:
            print("error: check the function install_db_extensions()")

