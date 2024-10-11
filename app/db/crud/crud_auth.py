import random

from typing import Callable, Any
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import selectinload


from db.schemas import (
     ResponseModel,
     QuestionSchema,
     AnswerSchema,
     UserModel
)
from db.models import User
from db.session import Session
from core import security



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
     
     
     @classmethod
     async def __questions_answers_sort(cls, data: dict) -> dict:
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

     
     
     async def create_new_user(
          self,
          username: str,
          password: str
     ) -> UserModel:
          async with self.session.begin() as db:
               model = {
                    'id': random.randint(10000, 100000000),
                    'username': username,
                    'password': await security.hashed.hashed_password(password),
                    'superuser': False
               }
               sttm = (
                    insert(User).values(**model)
               )
               await db.execute(sttm)
          return UserModel(**model)
          
          
          
     
     @id_or_username
     async def user_exists(self, **kwargs: Any) -> bool:
          async with self.session() as db:
               result = await db.execute(kwargs.get('sttm'))
               if result.scalar():
                    return False
          return True
     
     
     
     @id_or_username
     async def verify(self, **kwargs: Any) -> str | UserModel:
          async with self.session() as db:
               result = await db.execute(kwargs.get('sttm'))
               scalar = result.scalar()
               
               verify = await security.hashed.verify_hashed_passowrd(
                    password=kwargs.get('password'),
                    hashed_password=scalar.password
               )
               if verify:
                    return UserModel(**scalar.__dict__)
               return 'Invalid password or username!'
          
          
          
     async def delete_user(self, id: int) -> ResponseModel:
          async with self.session.begin() as db:
               sttm = (
                    delete(User).
                    where(User.id == id)
               )
               await db.execute(sttm)
          return ResponseModel(code=511, detail='Deleted user success!')
               
          
          
          
     @id_or_username
     async def get_user(self, **kwargs: Any) -> str | UserModel:
          async with self.session() as db:
               sttm = kwargs.get('sttm').options(
                    selectinload(User.user_questions),
                    selectinload(User.user_answers)
               )
               result = await db.execute(sttm)
               scalar = result.scalar()  
               
               if not scalar:
                    return 'User not found!'
               
               scalar_dict = scalar.__dict__
               data = await self.__questions_answers_sort(data=scalar_dict)
          return UserModel(**data)
          
     
     
     
auth_crud = CrudUser()
