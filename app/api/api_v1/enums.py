
from enum import Enum
from fastapi import HTTPException, status




class Mode(Enum):
     LOGIN = HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail='Invalid password or user.'
     )
     SIGNUP = HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail='User exists.'
     )


class CategoryEnum(Enum):
     SPORT = 'sport'
     GAMES = 'games'
     PROGRAMMING = 'programming'
     CLOTH = 'cloth'