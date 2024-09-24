
from typing import Annotated
from fastapi import Depends, APIRouter

from db.schemas import ResponseModel, QuestionSchema
from api.dependencies.forum import forum_depend

 
router = APIRouter(tags=['Forum'], prefix='/api/v1/forum/question')



@router.post('/create', response_model=ResponseModel)
async def create_question(
     create_data: Annotated[ResponseModel, Depends(forum_depend.create_question_depend)]
):
     return create_data



@router.patch('/update/{id_question}', response_model=ResponseModel)
async def update_question(
     update_data: Annotated[ResponseModel, Depends(forum_depend.change_question_depend)]
):
     return update_data



@router.get('/get/{id_question}', response_model=QuestionSchema)
async def get_question(
     get_data: Annotated[QuestionSchema, Depends(forum_depend.get_question_depend)]
):
     return get_data



@router.delete('/delete/{id_question}', response_model=ResponseModel)
async def delete_question(
     delete_data: Annotated[ResponseModel, Depends(forum_depend.delete_question_depend)]
):
     return delete_data



@router.get('/user_questions', response_model=ResponseModel | list[QuestionSchema])
async def get_questions_at_user(
     get_ques_data: Annotated[
          ResponseModel | list[QuestionSchema], 
          Depends(forum_depend.get_questions_at_user_depend)
     ]
):
     return get_ques_data



@router.patch('/change_category', response_model=ResponseModel)
async def change_category(
     change_data: Annotated[ResponseModel, Depends(forum_depend.change_category_depend)]
):
     return change_data