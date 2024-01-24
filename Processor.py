"""Processor base class
• Assumption that the output of run has __add__ defined
"""

from abc import abstractstaticmethod
from typing import Any, List, Optional
from glob import glob
import logging
import sys

from utils import cfg_to_paths

class Processor:
  @abstractstaticmethod
  def run(path: str) -> Optional[Any]:
    # result should define __add__
    pass

  @classmethod
  def run_config(cls, cfg) -> Any:
    agg = None
    for path in cfg_to_paths(cfg):
      try:
        res = cls.run(path)
        assert hasattr(res, '__add__') and callable(getattr(res, '__add__')), f"__add__ not defined on result for {cls}"

        if res is None:
          continue

        if agg is None:
          agg = res
        else:
          agg += res
      except Exception as e:
        print(f'Failure on {path}')
        print(e)

    return agg

  @classmethod
  def mk_logger(cls, level: int = logging.INFO) -> logging.Logger:
    lg = logging.getLogger(cls.__name__)
    lg.setLevel(logging.INFO)
    lg.addHandler( logging.StreamHandler(sys.stdout) )

    return lg