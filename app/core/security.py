from typing import Any
import bcrypt
import jwt

from app.core.config import settings



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
          iat: str, 
          exp: int, 
          perm: str = 'user'
     ) -> str:
          data = {
               'sub': sub,
               'iat': iat,
               'exp':  exp,
               'perm':  perm
          }
          token = jwt.encode(
               payload=data,
               key=settings.secret,
               algorithm=settings.alg
          )
          return token