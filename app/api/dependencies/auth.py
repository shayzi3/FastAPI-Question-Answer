
from typing import Any, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Query, status

from db.crud import crud
from core.security import Jwt
from api.api_v1.enums import Mode
from db.schemas import Token, UserModel
from core.auth import oauth_scheme




class AuthDepends:
     
     @classmethod
     async def login_depend(
          cls,
          form: Annotated[OAuth2PasswordRequestForm, Depends()]
     ) -> UserModel:
          
          await cls.exists(form.username, mode=Mode.LOGIN)
          
          verify = await crud.verify(
               username=form.username,
               password=form.password
          )
          if not verify:
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Invalid password!'
               )
          return verify
     
     
     @classmethod
     async def signup_depend(
          cls,
          form: Annotated[OAuth2PasswordRequestForm, Depends()]
     ) -> UserModel:
          
          await cls.exists(form.username, mode=Mode.SIGNUP)
          
          model = await crud.create_new_user(
               username=form.username,
               password=form.password
          )
          return model
     
     
     @classmethod
     async def get_user_depend(
          cls,
          scheme: Annotated[str, Depends(oauth_scheme)],
          id: int | None = None,
          username: str | None = None
     ) -> UserModel:
          if not id and not username:
               token = await Jwt.decode_access_token(scheme)
               user = await crud.get_user(id=token.sub)
               
          else:
               user = await crud.get_user(id=id, username=username)
               if not user:
                    raise HTTPException(
                         status_code=status.HTTP_404_NOT_FOUND,
                         detail='User not found.'
                    )
          return user


     @staticmethod
     async def exists(username: str, mode: Mode) -> bool | None:
          exists = await crud.user_exists(username=username)
          
          if mode == Mode.LOGIN:
               if exists:
                    raise mode.value
               
          elif mode == Mode.SIGNUP:
               if not exists:
                    raise mode.value
               
               
               
     @staticmethod
     async def get_token(
          sub: Any, 
          exp: int | None = None,
          superuser: bool = False
     ) -> Token:
          token = await Jwt.get_access_token(sub=sub, exp=exp, superuser=superuser)
               
          return Token(access_token=token, token_type='bearer')
     
     
     
               
auth_depends = AuthDepends()