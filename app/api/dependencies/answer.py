
from typing import Annotated
from fastapi import HTTPException, status, Depends, Body

from core.auth import oauth_scheme
from core.security import Jwt
from db.schemas import ResponseModel, AnswerSchema
from db.crud.crud_answer import crud_answer




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
     
     
     @staticmethod
     async def get_answer_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          id_answer: int
     ) -> AnswerSchema:
          await Jwt.decode_access_token(token)
          
          get = await crud_answer.answer_get(answer_id=id_answer)
          if isinstance(get, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=get
               )
          return get
     
     
     @staticmethod
     async def update_answer_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          new_answer: Annotated[str, Body(embed=True)],
          id_answer: int
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          update = await crud_answer.update_answer(
               answer_id=id_answer,
               user_id=data.sub,
               answer=new_answer
          )
          if isinstance(update, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=update
               )
          return update
     
     
     @staticmethod
     async def delete_answer_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          id_answer: int
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          delete = await crud_answer.delete_answer(
               answer_id=id_answer,
               user_id=data.sub
          )
          if isinstance(delete, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=delete
               )
          return delete
     
     
     @staticmethod
     async def get_user_answers_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          id_user: int | None = None,
          username: str | None = None
     ) -> list[AnswerSchema | None]:
          await Jwt.decode_access_token(token)
          
          answer = await crud_answer.get_answers_user(
               id=id_user,
               username=username
          )
          if isinstance(answer, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=answer
               )
          return answer
          
          
          
          
          
     
     
     
answer_depend = AnswerDepend()