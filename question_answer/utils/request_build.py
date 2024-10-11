
from question_answer.types import (
     ModeUrl, 
     ModeArguments,
     Token,
     Error,
     ServerResponse,
     RequestMethods
)
from question_answer.utils import returns




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
     ) -> returns.return_auth:
          """Requests for auth

          Args:
              mode_url (ModeUrl): part of url for self.__base_url
              req_method (RequestMethods): POST, GET, DELETE
              token (str | None, optional): for delete and get_user. Defaults to None.
              id (str | None, optional): for search user. Defaults to None.
              username (str | None, optional): for login or signup and for search user. Defaults to None.
              password (str | None, optional): for login and signup. Defaults to None.

          Returns:
              returns.return_auth: Token, Error, ServerResponse
          """
          
          headers = {'Authorization': f'Bearer {token}'} if token else None   
          data = {
               'username': username,
               'password': password
          } if username and password else None
          
          
          url = self.__base_url + mode_url.value
          if id:
               url = self.__base_url + mode_url.value + ModeArguments.GET_USER_BY_ID.value + id
               
          elif username:
               url = self.__base_url + mode_url.value + ModeArguments.GET_USER_BY_NAME.value + username
                    
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
          if mode_url == ModeUrl.LOGIN or mode_url == ModeUrl.SIGNUP:
               return Token(**response.json())
          
          elif mode_url == ModeUrl.DELETE:
               return ServerResponse(
                    status_code=response.status_code,
                    detail=response.json()['detail']
               )
     

          
          