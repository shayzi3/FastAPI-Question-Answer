
from typing import Annotated
from fastapi import Depends, APIRouter

from db.schemas import ResponseModel, QuestionSchema
from api.dependencies.forum import forum_depend

 
router = APIRouter(tags=['Forum'], prefix='/api/v1/forum')



@router.post('/create', response_model=ResponseModel)
async def create_question(
     data: Annotated[ResponseModel, Depends(forum_depend.create_question_depend)]
):
     return data


@router.patch('/change/{id_question}', response_model=ResponseModel)
async def change_question(
     data: Annotated[ResponseModel, Depends(forum_depend.change_question_depend)]
):
     return data


@router.get('/question/{id_question}', response_model=QuestionSchema)
async def get_question(
     data: Annotated[QuestionSchema, Depends(forum_depend.get_question_depend)]
):
     return data


@router.delete('/delete/{id_question}', response_model=ResponseModel)
async def delete_question(
     data: Annotated[ResponseModel, Depends(forum_depend.delete_question_depend)]
):
     return data


@router.get('/user_questions', response_model=ResponseModel | list[QuestionSchema])
async def get_questions_at_user(
     data: Annotated[
          ResponseModel | list[QuestionSchema], 
          Depends(forum_depend.get_questions_at_user_depend)
     ]
):
     return data