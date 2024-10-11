
from enum import Enum
from requests import (
     Response,
     get,
     post,
     delete,
     patch
)



class ModeUrl(Enum):
     # Auth
     LOGIN = '/user/login'
     SIGNUP = '/user/signup'
     DELETE = '/user/delete'
     GET_USER = '/user/get'
     
     
class RequestMethods(Enum):
     GET: Response = get
     POST: Response = post
     DELETE: Response = delete
     PATCH: Response = patch
     
     
     
class ModeArguments(Enum):
     GET_USER_BY_ID = '?id='
     GET_USER_BY_NAME = '?username='