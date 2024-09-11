import json
import random
from typing import Any, Callable

from sqlalchemy import insert, select, update, delete

from db.models import User, Question
from db.schemas import UserModel, ResponseModel
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

     
     
     @classmethod
     async def create_new_user(
          cls,
          username: str,
          password: str
     ) -> UserModel:
          async with cls.session.begin() as db:
               model = {
                    'id': random.randint(1000000, 1000000000000),
                    'username': username,
                    'password': await hashed.hashed_password(password),
                    'questions': json.dumps([]),
                    'answers': json.dumps([]),
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
               result = await db.execute(kwargs.get('sttm'))
               scalar = result.scalar()               
               
          if scalar:
               return UserModel(**scalar.__dict__)
          return None
     
     
     
     
class CrudQuestion(Session):
     ...

     
     

crud = CrudUser()
crud_question = CrudQuestion()