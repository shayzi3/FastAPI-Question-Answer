
from typing import Annotated
from fastapi import APIRouter, Depends

from api.dependencies.admin import admin_depend
from db.schemas import ResponseModel
from db.crud.crud_admin import admin_crud


router_admin = APIRouter(
     tags=['Admin'], 
     prefix='/api/v1/admin', 
     dependencies=[Depends(admin_crud.is_superuser)]
)


@router_admin.delete(path='/delete_question_answer', response_model=ResponseModel)
async def delete_question_answer(
     delete_data: Annotated[ResponseModel, Depends(admin_depend.delete_question_answer_depend)]
):
     return delete_data


@router_admin.patch(path='/update_question_answer', response_model=ResponseModel)
async def update_question_answer(
     update_data: Annotated[ResponseModel, Depends(admin_depend.update_question_answer_depend)]
):
     return update_data


@router_admin.delete(path='/delete_user', response_model=ResponseModel)
async def delete_user(
     delete_data: Annotated[ResponseModel, Depends(admin_depend.delete_user_depend)]
):
     return delete_data