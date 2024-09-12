from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.auth import auth_depends
from db.schemas import Token, UserModel, ResponseModel



router = APIRouter(tags=['Auth'], prefix='/api/v1/user')



@router.post('/login', response_model=Token)
async def login(
     data: Annotated[UserModel, Depends(auth_depends.login_depend)]
):
     
     return await auth_depends.get_token(sub=data.id)

     


@router.post('/signup', response_model=Token)
async def signup(
     data: Annotated[UserModel, Depends(auth_depends.signup_depend)]
):
     
     return await auth_depends.get_token(sub=data.id)



@router.delete('/delete', response_model=ResponseModel)
async def delete(
     data: Annotated[ResponseModel, Depends(auth_depends.delete_depend)]
):
     
     return data




@router.get('/get', response_model=UserModel)
async def get_me(
     data: Annotated[UserModel, Depends(auth_depends.get_user_depend)]
):
     
     return data
     

     
     