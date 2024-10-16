import random

from typing import Callable, Any
from sqlalchemy import select, delete, update, text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import  AsyncSession
from string import digits, punctuation, whitespace


from db.schemas import (
     ResponseModel,
     QuestionSchema,
     AnswerSchema
)
from db.models import User, Question
from db.session import Session



class CrudQuestion(Session):
     
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
     async def __update_question_at_user(
          id: int, 
          question: Question, 
          session: AsyncSession
     ) -> None:
          sttm = (
               select(User).
               filter_by(id=id).
               options(selectinload(User.user_questions))
          )
          response = await session.execute(sttm)
          scalar = response.scalar()
          scalar.user_questions.append(question)
          
     
     
     async def question_create(
          self, 
          question: str, 
          user_id: int, 
          category: str
     ) -> ResponseModel:
          async with self.session.begin() as db:
               question_object = {
                    'question_id': random.randint(100000, 100000000),
                    'question': question,
                    'user_id': user_id,
                    'category': category
               }
               ques = Question(**question_object)
               await self.__update_question_at_user(
                    id=user_id,
                    question=ques,
                    session=db
               )
               db.add(ques)          
          return ResponseModel(code=201, detail='Question created success.')
     
     
     async def update_question(
          self, 
          question_id: int, 
          user_id: int, 
          new_question: str
     ) -> ResponseModel | str:
          async with self.session.begin() as db:
               sttm_question = select(Question).filter_by(
                    question_id=question_id,
                    user_id=user_id
               )
               response = await db.execute(sttm_question)
               scalar = response.scalar()
               
               if not scalar:
                    return 'Question not found.'
               
               sttm = (
                    update(Question).
                    filter_by(question_id=question_id, user_id=user_id).
                    values(question=new_question)
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Question changed success.')
     
     
     async def question_get(
          self, 
          question_id: int
     ) -> QuestionSchema | str:
          async with self.session() as db:
               sttm = (
                    select(Question).
                    filter_by(question_id=question_id).
                    options(selectinload(Question.answers))
               )
               response = await db.execute(sttm)
               scalar = response.scalar()
               
               if not scalar:
                    return 'Question not found.'
               
               data = scalar.__dict__
               new_answers: list[AnswerSchema] = []
               
               for answ_ in data['answers']:
                    new_answers.append(AnswerSchema(**answ_.__dict__))
               data['answers'] = new_answers
          return QuestionSchema(**scalar.__dict__)
     

     
     async def del_question(
          self, 
          user_id: int, 
          question_id: int
     ) -> ResponseModel | str:
          async with self.session.begin() as db:
               sttm_exists = select(Question).filter_by(
                    question_id=question_id, 
                    user_id=user_id
               )
               response = await db.execute(sttm_exists)
               scalar = response.scalar()
               
               if not scalar:
                    return 'Question not found.'
               
               sttm = (
                    delete(Question).
                    filter_by(
                         question_id=question_id, 
                         user_id=user_id
                    )
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Question deleted success.')
     
     
     @id_or_username
     async def get_questions_user(
          self, 
          **kwargs: Any
     ) -> list[QuestionSchema] | str:
          async with self.session() as db:
               sttm = kwargs.get('sttm').options(
                    selectinload(User.user_questions)
               )
               response = await db.execute(sttm)
               scalar: User = response.scalar()
               
               if not scalar:
                    return 'User not found.'
               
               list_questions: list[QuestionSchema] = []
               for ques in scalar.user_questions:
                    list_questions.append(QuestionSchema(**ques.__dict__))
          return list_questions



     @id_or_username
     async def change_category_at_question(
          self,
          **kwargs: Any
     ) -> ResponseModel | str:
          async with self.session.begin() as db:
               sttm_exists = select(Question).filter_by(
                    question_id=kwargs.get('id_question'), 
                    user_id=kwargs.get('id')
               )
               response = await db.execute(sttm_exists)
               scalar = response.scalar()
               
               if not scalar:
                    return 'You cant change this question!'
               
               sttm = (
                    update(Question)
                    .filter_by(
                         question_id=kwargs.get('id_question'),
                         user_id=kwargs.get('id')
                    ).values(category=kwargs.get('category'))
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Success changed category.')
     
     
     async def questions_search(
          self,
          text_query: str
     ) -> list[QuestionSchema]:
          
          def sorted_tuple(
               question_id: int,
               question: str,
               category: str,
               user_id: int,
               answers: list | None = None
          ) -> QuestionSchema:
               
               return QuestionSchema(
                    question_id=question_id,
                    question=question,
                    category=category,
                    user_id=user_id,
                    answers=answers
               )
          
          async with self.session() as db:
               symbols = digits + punctuation + whitespace
               
               normal_text = text_query.strip(symbols).split()
               lower_text = [txt.lower() for txt in normal_text]
               
               sttm_normal = text(f"SELECT * FROM questions where REGEXP_LIKE(question, '{' | '.join(normal_text)}')")
               sttm_lower = text(f"SELECT * FROM questions where REGEXP_LIKE(question, '{' | '.join(lower_text)}')")
               
               response_n = await db.execute(sttm_normal)
               response_l = await db.execute(sttm_lower)
               result = set(response_n.all() + response_l.all())
               
          
               return [sorted_tuple(*arg) for arg in result] if result else []
     
     
crud_question = CrudQuestion()
