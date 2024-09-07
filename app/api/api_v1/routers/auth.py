from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.auth import auth_depends
from db.schemas import Token, UserModel



router = APIRouter(tags=['Auth'], prefix='/api/v1/user')



@router.post('/login', response_model=Token)
async def login(
     data: Annotated[UserModel, Depends(auth_depends.login_depend)]
) -> Token:
     
     return await auth_depends.get_token(sub=data.id)

     


@router.post('/signup', response_model=Token)
async def signup(
     data: Annotated[UserModel, Depends(auth_depends.signup_depend)]
) -> Token:
     
     return await auth_depends.get_token(sub=data.id)




@router.get('/me', response_model=UserModel)
async def get_me(
     data: Annotated[UserModel, Depends(auth_depends.get_me_depend)]
) -> UserModel:
     
     return data
     
     
     

     
     