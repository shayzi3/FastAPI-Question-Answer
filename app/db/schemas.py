
from pydantic import BaseModel
     
     
     
class UserModel(BaseModel):
     id: int
     username: str
     superuser: bool
     user_questions: list | None = None
     user_answers: list | None = None
     
     
     
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
     
     
class QuestionSchema(BaseModel):
     question_id: int
     question: str
     category: str
     user_id: int
     
     
class AnswerSchema(BaseModel):
     answer_id: int
     answer: str
     user_id: int
     question_id: int
     
     