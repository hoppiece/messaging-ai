import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)

    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str

    CORS_ALLOW_ORIGIN: str = "*"

    AWS_DEFAULT_REGION: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    DYNAMODB_ENDPOINT_URL: str | None = None  # for developing dynamodb-local

    # above does not use in hygeia
    OPENAI_API_KEY: str | None = None


settings = Settings()  # type: ignore
