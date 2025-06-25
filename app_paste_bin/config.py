import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(override=True)


@dataclass
class Config:
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


def load_env() -> Config:
    return Config(
        DB_USER=os.environ['DB_USER'],
        DB_PASS=os.environ['DB_PASS'],
        DB_HOST=os.environ['DB_HOST'],
        DB_PORT=os.environ['DB_PORT'],
        DB_NAME=os.environ['DB_NAME'],
        SECRET_KEY=os.environ['SECRET_KEY'],
    )


config = load_env()
