import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)

    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str

    CORS_ALLOW_ORIGIN: str = "*"


settings = Settings()  # type: ignore
