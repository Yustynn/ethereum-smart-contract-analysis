"""Processor base class
• Assumption that the output of run has __add__ defined
"""

from abc import abstractstaticmethod
from typing import Any, Optional
from slither import Slither
import logging
import sys

class Processor:
  @abstractstaticmethod
  def run(slither: Slither) -> Optional[Any]:
    # return value's class should define __add__
    pass

  @classmethod
  def mk_logger(cls, level: int = logging.INFO) -> logging.Logger:
    lg = logging.getLogger(cls.__name__)
    lg.setLevel(logging.INFO)
    lg.addHandler( logging.StreamHandler(sys.stdout) )

    return lg