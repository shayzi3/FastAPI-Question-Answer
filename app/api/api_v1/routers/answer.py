
from typing import Annotated
from fastapi import APIRouter, Depends

from db.schemas import ResponseModel
from api.dependencies.answer import answer_depend


router = APIRouter(tags=['Answers'], prefix='/api/v1/answer')



@router.post('/create', response_model=ResponseModel)
async def create_answer(
     data: Annotated[ResponseModel, Depends(answer_depend.create_answer_depend)]
):
     return data