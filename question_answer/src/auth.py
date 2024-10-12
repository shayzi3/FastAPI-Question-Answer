from question_answer.utils import (
     Request
)
from question_answer.types import (
     ModeUrl,
     ServerResponse,
     Error,
     RequestMethods,
     Token,
     ReadUser
)
from question_answer.utils import validate_arguments




class Auth(Request):
     __slots__ = (
          "_token"
     )
     
     def __init__(self, token: str | None = None) -> None:
          self._token = token
          super().__init__()
          
     
     @validate_arguments
     def login(
          self,
          username: str,
          password: str
     ) -> Token | Error | ServerResponse:
     
          response = self._request_auth(
               mode_url=ModeUrl.LOGIN,
               req_method=RequestMethods.POST,
               username=username,
               password=password,
          )
          if 'access_token' in response.__dict__.keys():
               self._token = response.access_token
          return response
          
          
     @validate_arguments
     def signup(
          self,
          username: str,
          password: str
     ) -> Token | Error | ServerResponse:
          
          response = self._request_auth(
               mode_url=ModeUrl.SIGNUP,
               req_method=RequestMethods.POST,
               username=username,
               password=password
          )
          if 'access_token' in response.__dict__.keys():
               self._token = response.access_token
          return response
          
     
     @validate_arguments
     def delete(
          self,
          token: str | None = None
     ) -> ServerResponse | Error:
          
          return self._request_auth(
               mode_url=ModeUrl.DELETE,
               req_method=RequestMethods.DELETE,
               token=self._token if not token else token
          )
         
          
     @validate_arguments
     def read_user(
          self,
          id: str | None = None,
          username: str | None = None,
          token: str | None = None
     ) -> ReadUser | Error:
          if not self._token:
               raise ValueError("Required argument token")
          
          return self._request_auth(
               mode_url=ModeUrl.GET_USER,
               req_method=RequestMethods.GET,
               id=id,
               username=username,
               token=self._token if not token else token
          )