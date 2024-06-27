import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)
    OPENAI_API_KEY: str

    # Above does not use in hygeia_ai
    LINE_CHANNEL_SECRET: str | None = None
    LINE_CHANNEL_ACCESS_TOKEN: str | None = None
    AWS_DEFAULT_REGION: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None


settings = Settings()  # type: ignore
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
