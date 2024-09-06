
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
     create_async_engine,
     async_sessionmaker,
     AsyncSession
)
from app.core.config import settings


engine = create_async_engine(settings.url)
session = async_sessionmaker(engine)
     
     
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
     async with session() as conn:
          yield conn

     