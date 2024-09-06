
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger, ForeignKey, String

from .schemas import Permission



class Base(AsyncAttrs, DeclarativeBase):
     pass



class User(Base):
     __tablename__ = 'users'
     
     
     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
     email: Mapped[str] = mapped_column(nullable=False)
     password: Mapped[str] = mapped_column(nullable=False)
     permissions: Mapped[Permission] = mapped_column(nullable=False)
     questions: Mapped[str] = mapped_column(nullable=False)
     answers: Mapped[str] = mapped_column(nullable=False)
     
     
    
     
class Question(Base):
     __tablename__ = 'questions'
     
     question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     question: Mapped[str] = mapped_column(nullable=False)
     id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)
     username: Mapped[str] = mapped_column(ForeignKey('users.username'), nullable=False, unique=True)
     answers: Mapped[str] = mapped_column(nullable=False)