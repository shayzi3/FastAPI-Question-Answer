
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import BigInteger, ForeignKey, String





class Base(AsyncAttrs, DeclarativeBase):
     
     def __repr__(self) -> str:
          string = ''
          for c in self.__table__.columns:
               string += f'{c.name}={getattr(self, c.name)} '
               
          return f'<{self.__class__.__name__} {string.strip()}>'





class User(Base):
     __tablename__ = 'users'
     
     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
     password: Mapped[str] = mapped_column(nullable=False)
     superuser: Mapped[bool] = mapped_column(nullable=False)
     
     user_questions: Mapped[list['Question']] = relationship(back_populates="user_question")
     user_answers: Mapped[list['Answer']] = relationship(back_populates="user_answer")
     
     
     
class Answer(Base):
     __tablename__ = 'answers'
     
     answer_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     answer: Mapped[str] = mapped_column(nullable=False)
     user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False, unique=True)
     question_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('questions.question_id'), nullable=False, unique=True)
     
     user_answer: Mapped['User'] = relationship(back_populates="user_answers")  
     question: Mapped['Question'] = relationship(back_populates='answers')   
     
     
     
class Question(Base):
     __tablename__ = 'questions'
     
     question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     question: Mapped[str] = mapped_column(nullable=False)
     category: Mapped[str] = mapped_column(nullable=False)
     user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False, unique=True)

     user_question: Mapped['User'] = relationship(back_populates="user_questions")
     answers: Mapped[list['Answer']] = relationship(back_populates='question')
     
     
