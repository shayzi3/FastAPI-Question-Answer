
from typing import Annotated, Callable
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, update, delete

from db.models import User, Question, Answer
from db.session import Session
from core.auth import oauth_scheme
from core.security import Jwt
from api.api_v1.enums import AnswerQuestion
from db.schemas import ResponseModel


class CrudAdmin(Session):
     
     @staticmethod
     def statement_delete(func: Callable) -> ResponseModel:
          async def wrapper(*a, **kw) -> ResponseModel:     
               del_answers = None
                         
               if kw.get('mode') == AnswerQuestion.ANSWER:
                    sttm_select = select(Answer).filter_by(answer_id=kw.get('id'))
                    sttm_delete = delete(Answer).filter_by(answer_id=kw.get('id'))
                    
               else:
                    sttm_select = select(Question).filter_by(question_id=kw.get('id'))
                    
                    del_answers = delete(Answer).filter_by(question_id=kw.get('id'))
                    sttm_delete = delete(Question).filter_by(question_id=kw.get('id'))
                    
               kw.update(
                    {
                         'sttm_select': sttm_select,
                         'sttm_delete': sttm_delete,
                         'del_answers': del_answers
                    }
               )
               return await func(*a, **kw)
          return wrapper
     
     
     @staticmethod
     def statement_update(func: Callable) -> Callable:
          async def wrapper(*a, **kw) -> ResponseModel:
               mode: AnswerQuestion = kw.get('mode')
               
               if mode == AnswerQuestion.ANSWER:
                    sttm_select = select(Answer).filter_by(answer_id=kw.get('id'))
                    sttm_update = (
                         update(Answer).
                         filter_by(answer_id=kw.get('id')).
                         values(answer=kw.get('text'))
                    )
               else:
                    sttm_select = select(Question).filter_by(question_id=kw.get('id'))
                    sttm_update = (
                         update(Question).
                         filter_by(question_id=kw.get('id')).
                         values(question=kw.get('text'))
                    )
                     
               kw.update(
                    {
                         'sttm_select': sttm_select,
                         'sttm_update': sttm_update
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

               

     
     
     
admin_crud = CrudAdmin()