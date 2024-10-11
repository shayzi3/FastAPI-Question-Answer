import random

from typing import Callable
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
     Question,
     Answer,
     User
)
from db.schemas import (
     ResponseModel,
     AnswerSchema
)
from db.session import Session


class CrudAnswer(Session):
     
     @staticmethod
     def id_or_username(func: Callable) -> Callable:
          async def wrapper(*args, **kwagrs) -> Callable:
               if 'id' in kwagrs.keys() and kwagrs.get('id'):
                    sttm = select(User).filter_by(id=kwagrs.get('id'))
                         
               elif 'username' in kwagrs.keys() and kwagrs.get('username'):
                    sttm = select(User).filter_by(username=kwagrs.get('username'))
                              
               kwagrs.update({'sttm': sttm})
               return await func(__class__, **kwagrs)
          return wrapper
     
     
     @staticmethod
     async def __question_exists(
          ques_id: int,
          user_id: int,
          session: AsyncSession
     ) -> None | Question:
          sttm_exists = select(Question).filter_by(
               question_id=ques_id
          ).options(selectinload(Question.answers))
          
          response = await session.execute(sttm_exists)
          scalar = response.scalar()
          
          if not scalar:
               return 'Not found question or user.'
          
          if scalar.user_id == user_id:
               return 'You cant add answer to your question!'
               
          return scalar
     
     
     async def add_answer(
          self,
          question_id: int,
          answer: str,
          user_id: int
     ) -> ResponseModel:
          async with self.session.begin() as db:
               scalar = await self.__question_exists(ques_id=question_id, session=db, user_id=user_id)
               if isinstance(scalar, str):
                    return scalar
               
               answer_object = {
                    'answer_id': random.randint(100000, 100000000000000),
                    'answer': answer,
                    'user_id': user_id,
                    'question_id': question_id
               }
               ans = Answer(**answer_object)
               scalar.answers.append(ans)
               
               db.add(ans)
          return ResponseModel(code=200, detail='Answer add success.')
               
     
     
     async def answer_get(
          self,
          answer_id: int
     ) -> AnswerSchema | str:
          async with self.session() as db:
               sttm = (
                    select(Answer).
                    filter_by(
                         answer_id=answer_id
                    ).options(selectinload(Answer.question))
               )
               response = await db.execute(sttm)
               scalar = response.scalar()
               
               if not scalar:
                    return 'Answer not found.'
          return AnswerSchema(**scalar.__dict__)
     
     
     async def update_answer(
          self,
          answer_id: int,
          user_id: int,
          answer: str
     ) -> ResponseModel | str:
          async with self.session.begin() as db:
               sttm = (
                    select(Answer).
                    filter_by(
                         answer_id=answer_id,
                         user_id=user_id
                    )
               )
               response = await db.execute(sttm)
               scalar = response.scalar()
               
               if not scalar:
                    return 'User or question not found.'
               
               sttm_update = (
                    update(Answer).
                    filter_by(
                         answer_id=answer_id,
                         user_id=user_id
                    ).values(answer=answer)
               )
               await db.execute(sttm_update)
          return ResponseModel(code=200, detail='Answer updated success!')
     
     
     async def delete_answer(
          self,
          answer_id: int,
          user_id: int
     ) -> ResponseModel | str:
          async with self.session.begin() as db:
               sttm = (
                    select(Answer).
                    filter_by(
                         answer_id=answer_id,
                         user_id=user_id
                    )
               )
               response = await db.execute(sttm)
               scalar = response.scalar()
               
               if not scalar:
                    return 'Invalid question or you cant delete this question.'
               
               sttm_delete = (
                    delete(Answer).
                    filter_by(
                         answer_id=answer_id,
                         user_id=user_id
                    )
               )
               await db.execute(sttm_delete)
          return ResponseModel(code=200, detail='Answer deleted success!')
     
     
     @id_or_username
     async def get_answers_user(
          self,
          **kwargs
     ) -> list[AnswerSchema | None]:
          async with self.session() as db:
               sttm = kwargs.get('sttm').options(
                    selectinload(User.user_answers)
               )
               response = await db.execute(sttm)
               scalar: User = response.scalar()
               
               if not scalar:
                    return 'User not found'
               
               list_answers = []
               for answ in scalar.user_answers:
                    list_answers.append(AnswerSchema(**answ.__dict__))
          return list_answers
               
                 
answer_crud = CrudAnswer()