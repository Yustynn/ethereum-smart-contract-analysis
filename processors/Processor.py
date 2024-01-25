from abc import ABC, abstractmethod
from slither import Slither
from Monoid import Monoid
import logging

class Processor(ABC):
  @staticmethod
  @abstractmethod
  def run(slither: Slither) -> Monoid:
    pass

  @classmethod
  def mk_logger(cls, level: int = logging.INFO) -> logging.Logger:
    lg = logging.getLogger(cls.__name__)
    lg.setLevel(level=level)

    return lg