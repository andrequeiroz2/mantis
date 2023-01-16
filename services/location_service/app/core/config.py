from pydantic import BaseSettings
from dotenv import find_dotenv, load_dotenv
import os
from functools import lru_cache


class Settings(BaseSettings):

    load_dotenv(find_dotenv(".env.location"), override=True)

    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))
    LOGLEVEL = os.environ.get("LOGLEVEL")
    APITITLE = os.environ.get("APITITLE")
    DEBUG = os.environ.get("DEBUG")

    DBDIALECT = os.environ.get("DBDIALECT")
    DBHOST = os.environ.get("DBHOST")
    DBUSER = os.environ.get("DBUSER")
    DBPASSWORD = os.environ.get("DBPASSWORD")
    DBPORT = int(os.environ.get("DBPORT"))
    DBBASE = os.environ.get("DBBASE")

    SQLALCHEMY_DATABASE_STR: str = (
        f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBBASE}"
    )


@lru_cache
def settings_get() -> Settings:
    return Settings()


settings = settings_get()
