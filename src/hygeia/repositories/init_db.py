from sqlmodel import SQLModel

from hygeia import models  # noqa
from hygeia.botconf import engine


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
