
from question_answer.src import (
     Answer,
     Auth,
     Question
)



class QuestionAnswer(Auth):
     def __init__(self) -> None:
          super().__init__()
     
     @property
     def token(self) -> str | None:
          return self._token
          
     @property
     def answer(self):
          return Answer(self.token)
     
     @property
     def question(self):
          return Question(self.token)
          
     
     
     