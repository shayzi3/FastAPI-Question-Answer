

from pydantic import BaseModel



class Token(BaseModel):
     access_token: str
     token_type: str
     
     
class Error(BaseModel):
     status_code: int
     detail: str
     
     
class ServerResponse(BaseModel):
     status_code: int
     detail: str