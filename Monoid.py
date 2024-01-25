from abc import ABC, abstractmethod

class Monoid(ABC):
  @abstractmethod
  def __add__(self, other):
    pass
  
  @classmethod
  @abstractmethod
  def neutral(cls):
    pass