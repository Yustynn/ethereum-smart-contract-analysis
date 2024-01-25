"""Processor base class
• Assumption that the output of run is a monoid instance
"""

from abc import abstractstaticmethod
from typing import Any, Optional
from slither import Slither
from Monoid import Monoid
import logging

class Processor:
  @abstractstaticmethod
  def run(slither: Slither) -> Monoid:
    # return value's class should define __add__
    pass

  @classmethod
  def mk_logger(cls, level: int = logging.INFO) -> logging.Logger:
    lg = logging.getLogger(cls.__name__)
    lg.setLevel(logging.INFO)

    return lg