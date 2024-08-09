from hygeia import models
from hygeia.botconf import engine
from sqlmodel import SQLModel


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
