

from abc import ABC, abstractmethod


class AbstractCrud(ABC):
     def __init__(self) -> None:
          super().__init__()
     
     @abstractmethod
     def create():
          pass
          
     @abstractmethod
     def read():
          pass
          
     @abstractmethod
     def update():
          pass
          
     @abstractmethod
     def delete():
          pass