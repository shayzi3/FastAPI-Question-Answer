
from typing import Annotated
from fastapi import Depends, APIRouter

from db.schemas import ResponseModel
from api.dependencies.forum import forum_depend

 
router = APIRouter(tags=['Forum'], prefix='/api/v1/forum')



@router.post('/create', response_model=ResponseModel)
async def create_question(
     data: Annotated[ResponseModel, Depends(forum_depend.create_question_depend)]
):
     return data
