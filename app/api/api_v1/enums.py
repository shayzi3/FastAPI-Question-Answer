
from enum import Enum
from fastapi import HTTPException, status




class Mode(Enum):
     LOGIN = HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail='User dont exists.'
     )
     SIGNUP = HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail='User exists.'
     )
