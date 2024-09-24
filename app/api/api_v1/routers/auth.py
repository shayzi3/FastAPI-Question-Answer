from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.auth import auth_depends
from db.schemas import Token, UserModel, ResponseModel



router = APIRouter(tags=['Auth'], prefix='/api/v1/user')



@router.post('/login', response_model=Token)
async def login(
     login_data: Annotated[UserModel, Depends(auth_depends.login_depend)]
):
     
     return await auth_depends.get_token(sub=login_data.id)

     


@router.post('/signup', response_model=Token)
async def signup(
     signup_data: Annotated[UserModel, Depends(auth_depends.signup_depend)]
):
     
     return await auth_depends.get_token(sub=signup_data.id)



@router.delete('/delete', response_model=ResponseModel)
async def delete(
     delete_data: Annotated[ResponseModel, Depends(auth_depends.delete_depend)]
):
     
     return delete_data




@router.get('/get', response_model=UserModel)
async def get_me(
     get_data: Annotated[UserModel, Depends(auth_depends.get_user_depend)]
):
     return get_data
     

     
     