from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


class BaseConfig(ABC):
    def __init__(self, db_host: str, db_port: str, db_user: str, db_pass: str,
                 db_name: str) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        pass

    @abstractmethod
    def get_session(self):
        pass


class SyncConfig(BaseConfig):
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_session(self) -> sessionmaker:
        sync_engine = create_engine(
            url=self.DATABASE_URL,
            echo=False
        )
        session_factory = sessionmaker(sync_engine)
        return session_factory


class AsyncConfig(BaseConfig):

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_session(self) -> async_sessionmaker:
        async_engine = create_async_engine(
            url=self.DATABASE_URL,
        )
        async_session_factory = async_sessionmaker(async_engine)
        return async_session_factory