

from typing import Annotated
from fastapi import Body, HTTPException, status

from db.crud.crud_admin import admin_crud
from api.api_v1.enums import AnswerQuestion
from db.schemas import ResponseModel



class AdminDepend:
     
     async def delete_question_answer_depend(
          self,
          id: int,
          mode: AnswerQuestion
     ) -> ResponseModel:          
          result = await admin_crud.delete_answer_or_question(
               id=id,
               mode=mode
          )
          if isinstance(result, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result
               )
          return result
     
     
     async def update_question_answer_depend(
          self,
          id: int,
          text: Annotated[str, Body(embed=True)],
          mode: AnswerQuestion
     ) -> ResponseModel:
          
          update = await admin_crud.update_question_or_answer(
               id=id,
               mode=mode,
               text=text
          )
          if isinstance(update, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=update
               )
          return update
     
     
     async def delete_user_depend(
          self,
          id: int | None = None,
          username: str | None = None
     ) -> ResponseModel:
          
          delete = await admin_crud.user_delete(
               id=id,
               username=username
          )
          if isinstance(delete, str):
               raise HTTPException(
                    status_code=404,
                    detail=delete
               )
          return delete
          
          


admin_depend = AdminDepend()