import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)
    OPENAI_API_KEY: str | None = None

    # Above does not use in hygeia_ai
    LINE_CHANNEL_SECRET: str | None = None
    LINE_CHANNEL_ACCESS_TOKEN: str | None = None
    MYSQL_SERVER: str | None = None
    MYSQL_USER: str | None = None
    MYSQL_PORT: int | None = None
    MYSQL_PASSWORD: str | None = None
    MYSQL_DATABASE: str | None = None


settings = Settings()  # type: ignore
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
