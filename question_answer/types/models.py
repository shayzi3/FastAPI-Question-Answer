
from dataclasses import dataclass



@dataclass
class Token:
     access_token: str
     token_type: str
     
     
     
@dataclass
class Error:
     status_code: int
     detail: str
     
     
     
@dataclass
class ServerResponse:
     status_code: int
     detail: str
     
     
     
@dataclass
class ReadUser:
     id: int
     username: str
     superuser: bool
     user_questions: list
     user_answers: list