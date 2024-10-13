
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
     
     # Question
     CREATE_QUESTION = '/forum/question/create'
     READ_QUESTION = '/forum/question/get'
     UPDATE_QUESTION = '/forum/question/update'
     DELETE_QUESTION = '/forum/question/delete'
     GET_QUESTION_USER = '/forum/question/user_questions'
     CHANGE_CATEGORY = '/forum/question/change_category'
     
     
class RequestMethods(Enum):
     GET: Response = get
     POST: Response = post
     DELETE: Response = delete
     PATCH: Response = patch
     
     
     
class ModeArguments(Enum):
     GET_BY_ID = '?id='
     GET_BY_NAME = '?username='
     CATEGORY = '?category='
     
     
     
class Category(Enum):
     SPORT = 'sport'
     GAMES = 'games'
     PROGRAMMING = 'programming'
     CLOTH = 'cloth'