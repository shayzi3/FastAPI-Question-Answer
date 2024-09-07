

from sqlalchemy.ext.asyncio import (
     create_async_engine,
     async_sessionmaker
)
from core.config import settings



class Session:
     engine = create_async_engine(settings.url)
     session = async_sessionmaker(engine)
     
     

     