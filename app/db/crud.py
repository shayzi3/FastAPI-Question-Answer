import random
from typing import Any, Callable

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Question, Answer
from db.schemas import (
     UserModel, 
     ResponseModel, 
     QuestionSchema,
     AnswerSchema
)
from core.security import hashed
from db.session import Session



class CrudUser(Session):
     
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
     async def __questions_answers_sort(data: dict) -> dict:
          if data['user_questions']:
               new_question: list[QuestionSchema] = []
                    
               for ques_ in data['user_questions']:
                    new_question.append(QuestionSchema(**ques_.__dict__))

               data['user_questions'] = new_question
               
          if data['user_answers']:
               new_answers: list[AnswerSchema] = []
               
               for answ_ in data['user_answers']:
                    new_answers.append(AnswerSchema(**answ_.__dict__))
                    
               data['user_answers'] = new_answers
          
          return data

     
     
     @classmethod
     async def create_new_user(
          cls,
          username: str,
          password: str
     ) -> UserModel:
          async with cls.session.begin() as db:
               model = {
                    'id': random.randint(1000000, 100000000000000000),
                    'username': username,
                    'password': await hashed.hashed_password(password),
                    'superuser': False
               }
               sttm = (
                    insert(User).values(**model)
               )
               await db.execute(sttm)
               
          return UserModel(**model)
          
          
          
     
     @classmethod
     @id_or_username
     async def user_exists(cls, **kwargs: Any) -> bool:
          async with cls.session() as db:
               result = await db.execute(kwargs.get('sttm'))
               if result.scalar():
                    return False
          return True
     
     
     
     @classmethod
     @id_or_username
     async def verify(cls, **kwargs: Any) -> None | UserModel:
          async with cls.session() as db:
               result = await db.execute(kwargs.get('sttm'))
               scalar = result.scalar()
               
               verify = await hashed.verify_hashed_passowrd(
                    password=kwargs.get('password'),
                    hashed_password=scalar.password
               )
               if verify:
                    return UserModel(**scalar.__dict__)
               return None
          
          
     @classmethod
     async def delete_user(cls, id: int) -> ResponseModel:
          async with cls.session.begin() as db:
               sttm = (
                    delete(User).
                    where(User.id == id)
               )
               await db.execute(sttm)
               
          return ResponseModel(code=200, detail='Deleted success!')
               
          
          
          
     @classmethod
     @id_or_username
     async def get_user(cls, **kwargs: Any) -> None | UserModel:
          async with cls.session() as db:
               sttm = kwargs.get('sttm').options(
                    selectinload(User.user_questions),
                    selectinload(User.user_answers)
               )
               result = await db.execute(sttm)
               scalar = result.scalar()  
               
               scalar_dict = scalar.__dict__
               data = await cls.__questions_answers_sort(data=scalar_dict)
               
          if scalar:
               return UserModel(**data)
          return None
     
     
     
     
class CrudQuestion(Session):
     
     @staticmethod
     def id_or_username(func: Callable) -> Callable:
          async def wrapper(*args, **kwagrs) -> Callable:
               print(kwagrs)
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
          
     
     
     @classmethod
     async def question_create(
          cls, 
          question: str, 
          user_id: int, 
          category: str
     ) -> ResponseModel:
          async with cls.session.begin() as db:
               question_object = {
                    'question_id': random.randint(10000000, 100000000000000),
                    'question': question,
                    'user_id': user_id,
                    'category': category
               }
               ques = Question(**question_object)
               await cls.__update_question_at_user(
                    id=user_id,
                    question=ques,
                    session=db
               )
               db.add(ques)          
          return ResponseModel(code=201, detail='Question created success.')
     
     
     @classmethod
     async def update_question(
          cls, 
          question_id: int, 
          user_id: int, 
          new_question: str
     ) -> ResponseModel | None:
          async with cls.session.begin() as db:
               sttm_question = select(Question).filter_by(
                    question_id=question_id,
                    user_id=user_id
               )
               response = await db.execute(sttm_question)
               scalar = response.scalar()
               
               if not scalar:
                    return None
               
               sttm = (
                    update(Question).
                    filter_by(question_id=question_id, user_id=user_id).
                    values(question=new_question)
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Question changed success.')
     
     
     @classmethod
     async def question_get(
          cls, 
          question_id: int
     ) -> QuestionSchema | None:
          async with cls.session() as db:
               sttm = (
                    select(Question).
                    filter_by(question_id=question_id).
                    options(selectinload(Question.answers))
               )
               response = await db.execute(sttm)
               scalar = response.scalar()
               
               if not scalar:
                    return None
               
               data = scalar.__dict__
               if data['answers']:
                    new_answers: list[AnswerSchema] = []
               
                    for answ_ in data['answers']:
                         new_answers.append(AnswerSchema(**answ_.__dict__))
                    
                    data['answers'] = new_answers
          return QuestionSchema(**scalar.__dict__)
     
     
     @classmethod
     async def del_question(
          cls, 
          user_id: int, 
          question_id: int
     ) -> ResponseModel:
          async with cls.session.begin() as db:
               sttm_exists = select(Question).filter_by(
                    question_id=question_id, 
                    user_id=user_id
               )
               response = await db.execute(sttm_exists)
               scalar = response.scalar()
               
               if not scalar:
                    return None
               
               sttm = (
                    delete(Question).
                    filter_by(
                         question_id=question_id, 
                         user_id=user_id
                    )
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Question deleted success.')
     
     
     @classmethod
     @id_or_username
     async def get_questions_user(
          cls, 
          **kwargs: Any
     ) -> str | ResponseModel | list[QuestionSchema]:
          async with cls.session() as db:
               sttm = kwargs.get('sttm').options(
                    selectinload(User.user_questions)
               )
               response = await db.execute(sttm)
               scalar: User = response.scalar()
               
               if not scalar:
                    return 'User not found.'
               
               if not scalar.user_questions:
                    return ResponseModel(code=200, detail='Questions at user not found.')
               
               list_questions = []
               for ques in scalar.user_questions:
                    list_questions.append(QuestionSchema(**ques.__dict__))
          return list_questions



     @classmethod
     @id_or_username
     async def change_category_at_question(
          cls,
          **kwargs: Any
     ) -> ResponseModel | None:
          async with cls.session.begin() as db:
               sttm_exists = select(Question).filter_by(
                    question_id=kwargs.get('id_question'), 
                    user_id=kwargs.get('id')
               )
               response = await db.execute(sttm_exists)
               scalar = response.scalar()
               
               if not scalar:
                    return None
               
               sttm = (
                    update(Question)
                    .filter_by(
                         question_id=kwargs.get('id_question'),
                         user_id=kwargs.get('id')
                    ).values(category=kwargs.get('category'))
               )
               await db.execute(sttm)
          return ResponseModel(code=200, detail='Success changed category.')
               
                            

class CrudAnswer(Session):
     
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
     
     
     @classmethod
     async def add_answer(
          cls,
          question_id: int,
          answer: str,
          user_id: int
     ) -> ResponseModel:
          async with cls.session.begin() as db:
               scalar = await cls.__question_exists(ques_id=question_id, session=db, user_id=user_id)
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
               
     
     
     @classmethod
     async def answer_get(
          cls,
          answer_id: int
     ) -> AnswerSchema | str:
          async with cls.session() as db:
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
     
     
     @classmethod
     async def update_answer(
          cls,
          answer_id: int,
          user_id: int,
          answer: str
     ) -> ResponseModel | str:
          async with cls.session.begin() as db:
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
     
     
          

     
     

crud = CrudUser()
crud_question = CrudQuestion()
crud_answer = CrudAnswer()