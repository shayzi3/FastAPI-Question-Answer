

from typing import Annotated
from fastapi import Depends, HTTPException, status

from db.crud.crud_admin import admin_crud
from api.api_v1.enums import AnswerQuestion
from db.schemas import ResponseModel
from core.auth import oauth_scheme
from core.security import Jwt



class AdminDepend:
     
     async def delete_question_answer_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          id: int,
          mode: AnswerQuestion
     ) -> ResponseModel:
          await Jwt.decode_access_token(token)
          
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


admin_depend = AdminDepend()