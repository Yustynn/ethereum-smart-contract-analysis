"""Processor base class
• Assumption that the output of run has __add__ defined
"""

from abc import abstractstaticmethod
from typing import Any, Optional
from datetime import datetime
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
    # setup error logger
    le = logging.getLogger(cls.__name__)
    le.setLevel(logging.INFO)
    handler = logging.FileHandler('err.log')
    le.addHandler(handler)


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
        le.info(f'{datetime.now()} [FAIL - {cls.__name__}: {path}] {e}')

    return agg

  @classmethod
  def mk_logger(cls, level: int = logging.INFO) -> logging.Logger:
    lg = logging.getLogger(cls.__name__)
    lg.setLevel(logging.INFO)
    lg.addHandler( logging.StreamHandler(sys.stdout) )

    return lg