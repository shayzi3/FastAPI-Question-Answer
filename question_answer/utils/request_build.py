
from question_answer.types import (
     ModeUrl, 
     ModeArguments,
     Token,
     Error,
     ServerResponse,
     RequestMethods,
     ReadUser,
     Category
)


class Request:
     __slots__ = (
          "__base_url",
     )
     
     def __init__(self) -> None:
          self.__base_url = 'http://127.0.0.1:8000/api/v1'
          
     def _request_auth(
          self,
          mode_url: ModeUrl,
          req_method: RequestMethods,
          token: str | None = None,
          id: str | None = None,
          username: str | None = None,
          password: str | None = None
     ) -> dict | Error:
          
          headers = {'Authorization': f'Bearer {token}'} if token else None
          data = {
               'username': username,
               'password': password
          } if username and password else None
          
          
          url = self.__base_url + mode_url.value
          if mode_url == ModeUrl.GET_USER:
               if id:
                    url = self.__base_url + mode_url.value + ModeArguments.GET_BY_ID.value + id
                    
               elif username:
                    url = self.__base_url + mode_url.value + ModeArguments.GET_BY_NAME.value + username
                    
          response = req_method(
               url=url,
               headers=headers,
               data=data
          )
          if response.status_code != 200:
               return Error(
                    status_code=response.status_code, 
                    detail=response.json()['detail']
               )
          return response.json()
          
          
     def _request_question(
          self,
          mode_url: ModeUrl,
          req_method: RequestMethods,
          token: str,
          category: Category | None = None,
          question: str | None = None,
          id_question: str | None = None,
          user_id: str | None = None,
          username: str | None = None
     ) -> list[dict] | dict | Error:
          
          headers = {'Authorization': f'Bearer {token}'}
          question_json = {'question':  question} if question else None

          if isinstance(category, Category):
               category = category.value
          
          url =  self.__base_url + mode_url.value
          if mode_url in [ModeUrl.READ_QUESTION, ModeUrl.DELETE_QUESTION, ModeUrl.UPDATE_QUESTION]:
               url += '/' + id_question
                    
                    
          elif mode_url == ModeUrl.CREATE_QUESTION:
               url += '?' + ModeArguments.CATEGORY.value + category
               
               
          elif mode_url == ModeUrl.GET_QUESTION_USER:
               if user_id:
                    url += ModeArguments.GET_BY_ID.value + user_id
                    
               elif username:
                    url += ModeArguments.GET_BY_NAME.value + username
               
               
          elif mode_url == ModeUrl.CHANGE_CATEGORY:
               url += '?id_question=' + id_question + '&' + ModeArguments.CATEGORY.value + category
               
          response = req_method(
               url=url,
               json=question_json,
               headers=headers
          )
          if response.status_code != 200:
               return Error(
                    status_code=response.status_code, 
                    detail=response.json()['detail']
               )
          return response.json()

               
               
               
               
          
               
          



     

          
          