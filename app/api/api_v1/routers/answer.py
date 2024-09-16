
from typing import Annotated
from fastapi import APIRouter, Depends

from db.schemas import ResponseModel, AnswerSchema
from api.dependencies.answer import answer_depend


router = APIRouter(tags=['Answers'], prefix='/api/v1/answer')



@router.post('/create', response_model=ResponseModel)
async def create_answer(
     data: Annotated[ResponseModel, Depends(answer_depend.create_answer_depend)]
):
     return data


@router.get('/get/{id_answer}', response_model=AnswerSchema)
async def get_answer(
     data: Annotated[AnswerSchema, Depends(answer_depend.get_answer_depend)]
):
     return data


@router.patch('/update/{id_answer}', response_model=ResponseModel)
async def update_answer(
     data: Annotated[ResponseModel, Depends(answer_depend.update_answer_depend)]
):
     return data


@router.delete('/delete/{id_answer}', response_model=ResponseModel)
async def delete_answer(
     data: Annotated[ResponseModel, Depends(answer_depend.delete_answer_depend)]
):
     return data