
from typing import Annotated
from fastapi import APIRouter, Depends

from db.schemas import ResponseModel, AnswerSchema
from api.dependencies.answer import answer_depend


router_answer = APIRouter(tags=['Answers'], prefix='/api/v1/answer')



@router_answer.post('/create', response_model=ResponseModel)
async def create_answer(
     create_data: Annotated[ResponseModel, Depends(answer_depend.create_answer_depend)]
):
     return create_data


@router_answer.get('/get/{id_answer}', response_model=AnswerSchema)
async def get_answer(
     get_data: Annotated[AnswerSchema, Depends(answer_depend.get_answer_depend)]
):
     return get_data


@router_answer.patch('/update/{id_answer}', response_model=ResponseModel)
async def update_answer(
     update_data: Annotated[ResponseModel, Depends(answer_depend.update_answer_depend)]
):
     return update_data


@router_answer.delete('/delete/{id_answer}', response_model=ResponseModel)
async def delete_answer(
     delete_data: Annotated[ResponseModel, Depends(answer_depend.delete_answer_depend)]
):
     return delete_data


@router_answer.get('/user_answers', response_model=list[AnswerSchema | None])
async def get_user_answers(
     get_user_data: Annotated[AnswerSchema, Depends(answer_depend.get_user_answers_depend)]
):
     return get_user_data