"""Processor base class
• Assumption that the output of run has __add__ defined
"""

from abc import abstractstaticmethod
from typing import Any, Optional
from glob import glob
import os
import logging
import sys

from config import ROOT_DIR

class Processor:
  @abstractstaticmethod
  def run(path: str) -> Optional[Any]:
    # result should define __add__
    pass

  @classmethod
  def run_config(cls, cfg) -> Any:
    # Retrieve file paths and run


    folder = os.path.join(ROOT_DIR, cfg['dir'])
    exclude_paths = cfg['exclude_paths'] if 'exclude_paths' in cfg else []

    paths = glob(os.path.join(folder, '*.sol')) + glob(os.path.join(folder, '**/*.sol'), recursive=True)
    paths = [
        p for p in paths
        if not any(p.startswith(os.path.join(folder, ep)) for ep in exclude_paths) # illegal path
        and not p.endswith('.t.sol') # exclude tests
    ]
    
    agg = None
    for path in paths:
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