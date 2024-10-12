
from question_answer.types import (
     ModeUrl, 
     ModeArguments,
     Token,
     Error,
     ServerResponse,
     RequestMethods,
     ReadUser
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
     ) -> Token | Error | ServerResponse | ReadUser:
          
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
               return ServerResponse(**response.json())
               
          elif mode_url == ModeUrl.GET_USER:
               return ReadUser(**response.json())

     

          
          