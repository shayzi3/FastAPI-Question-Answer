
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
     create_async_engine,
     async_sessionmaker,
     AsyncSession
)
from core.config import settings



class Session:
     engine = create_async_engine(settings.url)
     session = async_sessionmaker(engine)
     
     

     