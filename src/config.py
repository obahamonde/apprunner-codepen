from dotenv import load_dotenv
from pydantic import BaseSettings, BaseConfig, Field
import os

load_dotenv()


class Settings(BaseSettings):
    """Settings for the application
    """

    API_KEY: str = Field(default=os.environ.get("API_KEY"))
    FAUNA_SECRET: str = Field(default=os.environ.get("FAUNA_SECRET"))
    AUTH0_DOMAIN: str = Field(default=os.environ.get("AUTH0_DOMAIN"))
    AWS_ACCESS_KEY_ID: str = Field(default=os.environ.get("AWS_ACCESS_KEY_ID"))
    AWS_SECRET_ACCESS_KEY: str = Field(default=os.environ.get("AWS_SECRET_ACCESS_KEY"))
    AWS_REGION: str = Field(default=os.environ.get("AWS_REGION"))
    AWS_S3_BUCKET: str = Field(default=os.environ.get("AWS_S3_BUCKET"))
    REDIS_PASSWORD: str = Field(default=os.environ.get("REDIS_PASSWORD"))
    REDIS_HOST: str = Field(default=os.environ.get("REDIS_HOST"))
    REDIS_PORT: int = Field(default=os.environ.get("REDIS_PORT"))


    class Config(BaseConfig):
        env_file = ".env"
        file_encoding = "utf-8"


env = Settings()
