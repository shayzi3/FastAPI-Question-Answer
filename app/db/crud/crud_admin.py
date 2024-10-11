
from typing import Annotated, Callable
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, update, delete

from db.models import (
     User, 
     Question, 
     Answer
)
from db.session import Session
from db.schemas import ResponseModel
from core.auth import oauth_scheme
from core.security import Jwt
from api.api_v1.enums import AnswerQuestion


class CrudAdmin(Session):
     
     @staticmethod
     def statement_delete(func: Callable) -> ResponseModel:
          async def wrapper(*a, **kw) -> ResponseModel:    
               mode: AnswerQuestion = kw.get('mode') 
               class_ = None
                         
               if mode == AnswerQuestion.ANSWER:
                    class_ = Answer
                    req = {'answer_id': kw.get('id')}
                                        
               else:
                    class_ = Question
                    req = {'question_id': kw.get('id')}

                                        
               kw.update(
                    {
                         'sttm_select': select(class_).filter_by(**req),
                         'sttm_delete': delete(class_).filter_by(**req),
                         'del_answers': delete(Answer).filter_by(**req) if mode == AnswerQuestion.QUESTION else None
                    }
               )
               return await func(*a, **kw)
          return wrapper
     
     
     @staticmethod
     def statement_update(func: Callable) -> ResponseModel:
          async def wrapper(*a, **kw) -> ResponseModel:
               mode: AnswerQuestion = kw.get('mode')
               class_ = None
               
               if mode == AnswerQuestion.ANSWER:
                    class_ = Answer
                    
                    req = {'answer_id': kw.get('id')}
                    req_value = {'answer': kw.get('text')}
               
               else:
                    class_ = Question
                    
                    req = {'question_id': kw.get('id')}
                    req_value = {'question': kw.get('text')}
                    
                    
               kw.update(
                    {
                         'sttm_select': select(class_).filter_by(**req),
                         'sttm_update': update(class_).filter_by(**req).values(**req_value)
                    }
               )
               return await func(*a, **kw)
          return wrapper
     
     
     @staticmethod
     def statement_delete(func: Callable) -> ResponseModel | str:
          async def wrapper(*a, **kw) -> ResponseModel | str:
               if 'id' in kw.keys() and kw.get('id'):
                    req = {'id': kw.get('id')}
               
               elif 'username' in kw.keys() and kw.get('username'):
                    req = {'username': kw.get('username')}
                    
                    
               kw.update(
                    {
                         'sttm_select': select(User).filter_by(**req),
                         'sttm_delete': delete(User).filter_by(**req)
                    }
               )
               return await func(*a, **kw)
          return wrapper
     
     
     
     async def is_superuser(
          self,
          token: Annotated[str, Depends(oauth_scheme)]
     ) ->  bool:
          data = await Jwt.decode_access_token(token)
          
          if not data.perm:
               raise HTTPException(
                         status_code=status.HTTP_423_LOCKED,
                         detail='You not admin!'
                    )
          return True
     
     
     @statement_delete
     async def delete_answer_or_question(
          self,
          **kwargs
     ) -> ResponseModel:
          async with self.session.begin() as db:
               mode: AnswerQuestion = kwargs.get('mode')
               
               exists = await db.execute(kwargs.get('sttm_select'))
               scalar = exists.scalar()
               
               if not scalar:
                    return f'{mode.value} not found'
               
               if mode == AnswerQuestion.QUESTION:
                    await db.execute(kwargs.get('del_answers'))
               await db.execute(kwargs.get('sttm_delete'))
               
          return ResponseModel(code=200, detail=f'{mode.value} deleted.')
     
     
     @statement_update
     async def update_question_or_answer(
          self,
          **kwargs
     ) -> ResponseModel:
          async with self.session.begin() as db:
               mode: AnswerQuestion = kwargs.get('mode')
               
               exists = await db.execute(kwargs.get('sttm_select'))
               scalar = exists.scalar()
               
               if not scalar:
                    return f'{mode.value} not found'
               
               await db.execute(kwargs.get('sttm_update'))
          return ResponseModel(code=200, detail=f'{mode.value} updated success')
     
     
     @statement_delete
     async def user_delete(
          self,
          **kwargs
     ) -> ResponseModel:
          async with self.session.begin() as db:
               exists = await db.execute(kwargs.get('sttm_select'))
               scalar = exists.scalar()
               
               if not scalar:
                    return 'user not found'
               
               await db.execute(kwargs.get('sttm_delete'))
          return ResponseModel(code=200,  detail='user deleted')
     
admin_crud = CrudAdmin()