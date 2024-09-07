import bcrypt
import jwt

from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status

from core.config import settings
from db import crud
from db.schemas import TokenUser



class Hashed:
     
     @staticmethod
     async def hashed_password(password: str) -> str:
          return  bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
     
     
     @staticmethod
     async def verify_hashed_passowrd(password: str, hashed_password: str) -> bool:
          return bcrypt.checkpw(password.encode(), hashed_password.encode())
     
     
     

class JWT:
     
     @classmethod
     async def get_access_token(
          cls,
          sub: Any, 
          exp: int | None = None, 
          superuser: bool = False
     ) -> str:
          data = {
               'sub': sub,
               'iat': datetime.utcnow(),
               'exp':  datetime.utcnow() + timedelta(minutes=exp if exp else 30),
               'perm':  superuser
          }
          token = jwt.encode(
               payload=data,
               key=settings.secret,
               algorithm=settings.alg
          )
          return token
     
     
     @classmethod
     async def decode_access_token(cls, token: str) -> TokenUser:
          error = HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='You not authorized'
          )
          try:
               payload = jwt.decode(token, settings.secret, algorithms=settings.alg)
               
               sub = payload.get('sub')
               if not sub:
                    raise error
               
               user = TokenUser(**payload)
               
          except jwt.PyJWTError:
               raise error
          
          exists = await crud.crud.user_exists(id=user.sub)
          if exists:
               raise error

          return user

     
     
hashed = Hashed()
Jwt = JWT()