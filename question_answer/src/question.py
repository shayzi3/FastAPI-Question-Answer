

from question_answer.types import (
     Category,
     ModeUrl,
     RequestMethods,
     ServerResponse
)
from question_answer.utils import AbstractCrud, Request
from question_answer.utils import validate_arguments


class Question(AbstractCrud, Request):
     __slots__ = (
          "__token"
     )
     
     def __init__(self, token: str | None = None) -> None:
          if not isinstance(token, str):
               raise TypeError("token is required argument")

          self.__token = token
          super().__init__()
          
          
     @validate_arguments
     def create(
          self,
          question: str,
          category: Category | str,
          token: str | None = None
     ) -> ServerResponse:
          if isinstance(category, str):
               if category.upper() not in Category._member_names_:
                    raise ValueError(f"Not found category {category}")
               
          response = self._request_question(
               mode_url=ModeUrl.CREATE_QUESTION,
               req_method=RequestMethods.POST,
               question=question,
               category=category,
               token=self.__token if not token else token
          )
          return ServerResponse(
               status_code=response.get('code'),
               detail=response.get('detail')
          )
          
     
     
     @validate_arguments
     def read(self):
          return None
     
     
     @validate_arguments
     def update(self):
          return None
     
     
     @validate_arguments
     def delete(self):
          return None
