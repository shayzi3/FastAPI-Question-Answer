
from typing import Annotated
from fastapi import Depends, Body
from pydantic import Field

from db.crud import crud_question, crud
from core.auth import oauth_scheme
from core.security import Jwt
from db.schemas import ResponseModel
from api.api_v1.enums import CategoryEnum



class ForumDepends:
     
     @staticmethod
     async def create_question_depend(
          token: Annotated[str, Depends(oauth_scheme)],
          question: Annotated[str, Body(embed=True)],
          category: CategoryEnum
      ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          save = await crud_question.question_create(
               question=question,
               user_id=data.sub,
               category=category
          )
          return save
     
     
forum_depend = ForumDepends()
          
          



