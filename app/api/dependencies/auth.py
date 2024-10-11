
from typing import Any, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from db.crud.crud_auth import auth_crud
from db.schemas import Token, UserModel, ResponseModel
from api.api_v1.enums import Mode
from core.auth import oauth_scheme
from core.security import Jwt



 
class AuthDepends:
     
     
     async def login_depend(
          self,
          form: Annotated[OAuth2PasswordRequestForm, Depends()]
     ) -> UserModel:
          await self.exists(form.username, mode=Mode.LOGIN)
          
          verify = await auth_crud.verify(
               username=form.username,
               password=form.password
          )
          if isinstance(verify, str):
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=verify
               )
          return verify
     
     
     async def signup_depend(
          self,
          form: Annotated[OAuth2PasswordRequestForm, Depends()]
     ) -> UserModel:
          await self.exists(form.username, mode=Mode.SIGNUP)
          
          model = await auth_crud.create_new_user(
               username=form.username,
               password=form.password
          )
          return model
     
     
     async def delete_depend(
          self, 
          scheme: Annotated[str, Depends(oauth_scheme)]
     ) -> ResponseModel:
          token = await Jwt.decode_access_token(token=scheme)
          
          return await auth_crud.delete_user(id=token.sub)
     
     
     async def get_user_depend(
          self,
          scheme: Annotated[str, Depends(oauth_scheme)],
          id: int | None = None,
          username: str | None = None
     ) -> UserModel:
          token = await Jwt.decode_access_token(scheme)
          
          if not id and not username:
               user = await auth_crud.get_user(id=token.sub)
               
          else:
               user = await auth_crud.get_user(id=id, username=username)
               if isinstance(user, str):
                    raise HTTPException(
                         status_code=status.HTTP_404_NOT_FOUND,
                         detail=user
                    )
          return user


     @staticmethod
     async def exists(username: str, mode: Mode) -> None:
          exists = await auth_crud.user_exists(username=username)
          
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