
from typing import Annotated
from fastapi import HTTPException, status, Depends, Body

from core.auth import oauth_scheme
from core.security import Jwt
from db.schemas import ResponseModel
from db.crud import crud_answer




class AnswerDepend:
     
     @staticmethod
     async def create_answer_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          answer_text: Annotated[str, Body(embed=True)],
          id_question: int
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          answer_add = await crud_answer.add_answer(
               question_id=id_question,
               answer=answer_text,
               user_id=data.sub
          )
          if isinstance(answer_add, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=answer_add
               )
          return answer_add
     
     
answer_depend = AnswerDepend()