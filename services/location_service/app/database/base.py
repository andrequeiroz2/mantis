from sqlalchemy.ext.declarative import declarative_base
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.orm import Session
from pydantic import BaseSettings
from core.config import settings
from functools import lru_cache
from typing import Iterator


Base = declarative_base()


class DBSettings(BaseSettings):
    dialect = settings.DBDIALECT
    user = settings.DBUSER
    password = settings.DBPASSWORD
    host = settings.DBHOST
    port = settings.DBPORT
    database = settings.DBBASE
    database_uri: str = str(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")


def get_db() -> Iterator[Session]:
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    database_uri = DBSettings().database_uri
    return FastAPISessionMaker(database_uri)
