
from question_answer.utils import AbstractCrud, Request


class Answer(AbstractCrud, Request):
     __slots__ = (
          "__token"
     )
     
     def __init__(self, token: str | None = None) -> None:
          if not isinstance(token, str):
               raise ValueError("token is required argument")
          
          self.__token = token
          super().__init__()
          
     def create(self):
          return None
     
     def read(self):
          return None
     
     def update(self):
          return None
     
     def delete(self):
          return None