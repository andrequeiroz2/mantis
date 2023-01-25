from pydantic import BaseSettings
from dotenv import find_dotenv, load_dotenv
import os
from functools import lru_cache
import boto3
from botocore.config import Config

class Settings(BaseSettings):

    load_dotenv(find_dotenv(".env.location"), override=True)

    #API
    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))
    LOGLEVEL = os.environ.get("LOGLEVEL")
    APITITLE = os.environ.get("APITITLE")
    DEBUG = os.environ.get("DEBUG")

    #POSTGRES
    DBDIALECT = os.environ.get("DBDIALECT")
    DBHOST = os.environ.get("DBHOST")
    DBUSER = os.environ.get("DBUSER")
    DBPASSWORD = os.environ.get("DBPASSWORD")
    DBPORT = int(os.environ.get("DBPORT"))
    DBBASE = os.environ.get("DBBASE")

    #MIGRATE URL
    SQLALCHEMY_DATABASE_STR: str = (
        f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBBASE}"
    )

    # AWS S3 CONFIG
    S3_AWS_ACCESS_KEY_ID = os.environ.get("S3_AWS_ACCESS_KEY_ID")
    S3_AWS_SECRET_ACCESS_KEY = os.environ.get("S3_AWS_SECRET_ACCESS_KEY")
    S3_AWS_DEFAULT_REGION = os.environ.get("S3_AWS_DEFAULT_REGION")
    S3_SIGNATURE_VERSION = os.environ.get("S3_SIGNATURE_VERSION")
    S3_AWS_MAX_ATTEMPTS = int(os.environ.get("S3_AWS_MAX_ATTEMPTS"))
    S3_AWS_RETRY_MODE = os.environ.get("S3_AWS_RETRY_MODE")
    S3_AWS_BUCKET_NAME = os.environ.get("S3_AWS_BUCKET_NAME")
    S3_AWS_BUCKET_PATH = os.environ.get("S3_AWS_BUCKET_PATH")


@lru_cache
def settings_get() -> Settings:
    return Settings()


settings = settings_get()


s3_config = Config(
    region_name=settings.S3_AWS_DEFAULT_REGION,
    signature_version=settings.S3_SIGNATURE_VERSION,
    retries={
        'max_attempts': settings.S3_AWS_MAX_ATTEMPTS,
        'mode': settings.S3_AWS_RETRY_MODE,
    }
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.S3_AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_AWS_SECRET_ACCESS_KEY
)
