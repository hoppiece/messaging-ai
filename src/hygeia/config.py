import os

from pydantic import computed_field
from pydantic_core import MultiHostUrl
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
    TABLE_NAME: str = "hygeia-user"

    MYSQL_SERVER: str = "mysql"
    MYSQL_USER: str
    MYSQL_PORT: int = 3306
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    @computed_field  # type: ignore
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=f"{self.MYSQL_DATABASE}",
            query="charset=utf8mb4",
        )

    # above does not use in hygeia
    OPENAI_API_KEY: str | None = None


settings = Settings()  # type: ignore
