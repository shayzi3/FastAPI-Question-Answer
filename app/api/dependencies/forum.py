
from typing import Annotated
from fastapi import Depends, Body, HTTPException, status

from db.crud import crud_question
from core.auth import oauth_scheme
from core.security import Jwt
from db.schemas import ResponseModel, QuestionSchema
from api.api_v1.enums import CategoryEnum



class ForumDepends:
     error = HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail='Question not found!'
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
     
     
     @classmethod
     async def change_question_depend(
          cls,
          token: Annotated[str, Depends(oauth_scheme)],
          new_question: Annotated[str, Body(embed=True)],
          id_question: int
     ) ->  ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          change = await crud_question.update_question(
               question_id=id_question,
               user_id=data.sub,
               new_question=new_question
          )
          if not change:
               raise cls.error
          return change
     
     
     @classmethod
     async def get_question_depend(
          cls,
          token: Annotated[str, Depends(oauth_scheme)],
          id_question: int
     ) -> QuestionSchema:
          await Jwt.decode_access_token(token)
          
          get = await crud_question.question_get(
               question_id=id_question
          )
          if not get:
               raise cls.error
          return get
     
     
     @classmethod
     async def delete_question_depend(
          cls,
          token: Annotated[str, Depends(oauth_scheme)],
          id_question: int
     ) -> ResponseModel:
          data = await Jwt.decode_access_token(token)
          
          delete = await crud_question.del_question(
               user_id=data.sub,
               question_id=id_question
          )
          if not delete:
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You cant delete this question!'
               )
          return delete
     
     
     @classmethod
     async def get_questions_at_user_depend(
          cls,
          token: Annotated[str, Depends(oauth_scheme)],
          user_id: int | None = None,
          username: str | None = None
     ) -> ResponseModel | list[QuestionSchema]:
          data = await Jwt.decode_access_token(token)
          
          if not user_id and not username:
               user_id = data.sub
          
          get = await crud_question.get_questions_user(
               id=user_id,
               username=username
          )
          if isinstance(get, str):
               cls.error.detail = get
               raise cls.error
          return get
     
     
     @classmethod
     async def change_category_depend(
          cls,
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
          if not get:
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You cant delete this question!'
               )
          return get
     
     
forum_depend = ForumDepends()
          
          



