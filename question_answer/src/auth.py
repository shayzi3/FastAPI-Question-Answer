from question_answer.utils import (
     Request
)
from question_answer.types import (
     ModeUrl,
     ServerResponse,
     Error,
     RequestMethods,
     Token
)
from question_answer.utils import validate_arguments




class Auth(Request):
     def __init__(self, token: str | None = None) -> None:
          self._token = token
          super().__init__()
          
     
     @validate_arguments
     def login(
          self,
          username: str,
          password: str
     ) -> Token | Error | ServerResponse:
          """
          Args:
              username (str): your name
              password (str): your password

          Returns:
              return_auth: Token, Error
          """
          
          response = self._request_auth(
               mode_url=ModeUrl.LOGIN,
               req_method=RequestMethods.POST,
               username=username,
               password=password,
          )
          if 'access_token' in response.model_dump():
               self._token = response.access_token
          return response
          
          
     @validate_arguments
     def signup(
          self,
          username: str,
          password: str
     ) -> Token | Error | ServerResponse:
          """Create new account
          
          Args:
              username (str): create name
              password (str): create password

          Returns:
              return_auth: Token, Error
          """
          
          response = self._request_auth(
               mode_url=ModeUrl.SIGNUP,
               req_method=RequestMethods.POST,
               username=username,
               password=password
          )
          if 'access_token' in response.model_dump():
               self._token = response.access_token
          return response
          
     
     @validate_arguments
     def delete(
          self,
          token: str | None = None
     ) -> ServerResponse | Error:
          """Delete account

          Args:
              token (str): bearer token(from login)

          Returns:
              ServerResponse | Error
          """
          return self._request_auth(
               mode_url=ModeUrl.DELETE,
               req_method=RequestMethods.DELETE,
               token=self._token if not token else token
          )
         
          
     @validate_arguments
     def get_user(
          self,
          id: str | None = None,
          username: str | None = None,
          token: str | None = None
     ) -> ...:
          if not id and not username:
               raise ValueError("Either id or username must be provided")