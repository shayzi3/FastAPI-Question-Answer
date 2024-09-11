
from enum import Enum
from pydantic import BaseModel
     
     
     
class UserModel(BaseModel):
     id: int
     username: str
     questions: str
     answers: str
     superuser: bool
     
     
     
class UserModelExtend(UserModel):
     password: str
     
     

class Token(BaseModel):
     access_token: str
     token_type: str
     
     

class TokenUser(BaseModel):
     sub: int
     perm: bool
     
     

class ResponseModel(BaseModel):
     code: int 
     detail: str
     
     
     