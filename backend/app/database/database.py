from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import Engine
from typing import Generator, Optional
from pathlib import Path
from loguru import logger


class Database:

    def __init__(self) -> None:
        self._url: str = f"sqlite:///{Path(__file__).parent / 'database.db'}"
        self._engine: Optional[Engine] = None
    
    @property
    def session(self) -> Generator[Session, None, None]:
        if self._engine is None:
            raise RuntimeError("Database not initialized")
        with Session(self._engine) as session:
            yield session
    
    async def connect(self) -> None:
        """Connected to the database"""
        try:
            self._engine = create_engine(self._url)
            SQLModel.metadata.create_all(self._engine)
            logger.success("Database connected and initialized")
        except Exception as e:
            logger.warning(f"Error connecting to database: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from the database"""
        try:
            if self._engine is None: return
            self._engine.dispose()
            logger.success("Database disconnected")
        except Exception as e:
            logger.warning(f"Error disconnecting from database: {e}")
