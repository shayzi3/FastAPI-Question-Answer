
from typing import Annotated
from fastapi import Depends, Body, HTTPException, status

from db.crud.crud_forum import crud_question
from db.schemas import ResponseModel, QuestionSchema
from core.auth import oauth_scheme
from core.security import Jwt
from api.api_v1.enums import CategoryEnum



class ForumDepends:
     error = HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail='Question not found.'
     )
     

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
               category=category.value
          )
          return save
     
     
     async def change_question_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          question: Annotated[str, Body(embed=True)],
          id_question: int
     ) ->  ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          change = await crud_question.update_question(
               question_id=id_question,
               user_id=data.sub,
               new_question=question
          )
          if isinstance(change, str):
               raise self.error
          return change
     
     
     async def get_question_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          id_question: int
     ) -> QuestionSchema:
          await Jwt.decode_access_token(token)
          
          get = await crud_question.question_get(
               question_id=id_question
          )
          if isinstance(get, str):
               raise self.error
          return get
     
     
     async def delete_question_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          id_question: int
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          delete = await crud_question.del_question(
               user_id=data.sub,
               question_id=id_question
          )
          if isinstance(delete, str):
               raise self.error
          return delete
     
     
     async def get_questions_at_user_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          id: int | None = None,
          username: str | None = None
     ) -> list[QuestionSchema]:
          data = await Jwt.decode_access_token(token)
          
          if not id and not username:
               id = data.sub
          
          get = await crud_question.get_questions_user(
               id=id,
               username=username
          )
          if isinstance(get, str):
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=get
               )
          return get
     
     
     async def change_category_depend(
          self,
          token: Annotated[str, Depends(oauth_scheme)],
          id_question: int,
          category: CategoryEnum
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          get = await crud_question.change_category_at_question(
               id_question=id_question,
               category=category.value,
               id=data.sub
          )     
          if isinstance(get, str):
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=get
               )
          return get
     
     
forum_depend = ForumDepends()
          
          



