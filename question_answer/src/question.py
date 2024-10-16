

from question_answer.types import (
     Category,
     ModeUrl,
     RequestMethods,
     ServerResponse,
     Error,
     ReadQuestion
)
from question_answer.utils import AbstractCrud, Request
from question_answer.utils import validate_arguments




class Question(AbstractCrud, Request):
     __slots__ = (
          "__token"
     )
     
     def __init__(self, token: str | None = None) -> None:
          if not isinstance(token, str):
               raise ValueError("token is required argument")

          self.__token = token
          super().__init__()
          
          
     @validate_arguments
     def create(
          self,
          question: str,
          category: Category | str
     ) -> ServerResponse:
          if isinstance(category, str):
               if category.upper() not in Category._member_names_:
                    raise ValueError(f"Not found category {category}")
               
          response = self._request_question(
               mode_url=ModeUrl.CREATE_QUESTION,
               req_method=RequestMethods.POST,
               question=question,
               category=category,
               token=self.__token
          )
          return ServerResponse(
               status_code=response.get('code'),
               detail=response.get('detail')
          )
          
     
     @validate_arguments
     def read(
          self,
          id_question: str
     ) -> ReadQuestion | Error:
          
          response = self._request_question(
               mode_url=ModeUrl.READ_QUESTION,
               req_method=RequestMethods.GET,
               id_question=id_question,
               token=self.__token
          )
          if isinstance(response, Error):
               return response
          return ReadQuestion(**response)
     
     
     @validate_arguments
     def update(
          self,
          question: str,
          id_question: str
     ) -> ServerResponse | Error:
          
          response = self._request_question(
               mode_url=ModeUrl.UPDATE_QUESTION,
               req_method=RequestMethods.PATCH,
               question=question,
               id_question=id_question,
               token=self.__token
          )
          if isinstance(response, Error):
               return response
          
          return ServerResponse(
               status_code=response.get('code'),
               detail=response.get('detail')
          )
         
     
     
     @validate_arguments
     def delete(
          self,
          id_question: str
     ) -> ServerResponse | Error:
          
          response = self._request_question(
               mode_url=ModeUrl.DELETE_QUESTION,
               req_method=RequestMethods.DELETE,
               id_question=id_question,
               token=self.__token
          )
          if isinstance(response, Error):
               return response
          
          return ServerResponse(
               status_code=response.get('code'),
               detail=response.get('detail')
          )
          
          
     @validate_arguments
     def change_category(
          self,
          id_question: str,
          category: Category | str
     ) -> ServerResponse | Error:
          if isinstance(category, str):
               if category.upper() not in Category._member_names_:
                    raise ValueError(f"Not found category {category}")
               
          response = self._request_question(
               mode_url=ModeUrl.CHANGE_CATEGORY,
               req_method=RequestMethods.PATCH,
               id_question=id_question,
               category=category,
               token=self.__token
          )
          if isinstance(response, Error):
               return response
          
          return ServerResponse(
               status_code=response.get('code'),
               detail=response.get('detail')
          )
          
     
     
     @validate_arguments
     def read_user_questions(
          self,
          user_id: str | None = None,
          username: str | None = None
     ) -> list[ReadQuestion] | Error:
          
          response = self._request_question(
               mode_url=ModeUrl.GET_QUESTION_USER,
               req_method=RequestMethods.GET,
               user_id=user_id,
               username=username,
               token=self.__token
          )
          if isinstance(response, Error):
               return response
          
          if not response:
               return []
          return [ReadQuestion(**que) for que in response]
