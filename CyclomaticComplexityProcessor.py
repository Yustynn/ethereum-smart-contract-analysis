from slither import Slither
from slither.utils.code_complexity import compute_cyclomatic_complexity
from Processor import Processor

from dataclasses import dataclass
from statistics import mean, median
from typing import List, Optional
import solc_select_api

import logging
logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('CyclomaticComplexityProcessor')

@dataclass
class CyclomaticComplexityResult:
  total: int
  mean: float
  median: float
  num_functions: int
  raw: List[int]

  @staticmethod
  def from_ccs(ccs: List[int]) -> 'CyclomaticComplexityResult':
      return CyclomaticComplexityResult(
        total = sum(ccs),
        mean = mean(ccs),
        median = median(ccs),
        num_functions = len(ccs),
        raw = ccs
      )

  def __add__(self, other):
    return self.__class__.from_ccs(self.raw + other.raw)
    

def parse_version(path: str) -> Optional[str]:
  import re
  PATTERN_VERSION = r"\d+\.\d+\.\d+"

  with open(path) as f:
    lines = f.readlines()

  for l in lines:
    if not 'pragma' in lines:
      continue
    matches = re.findall(PATTERN_VERSION, l)

    if len(matches) > 0:
      version = matches[0]
      lg.info(f'Version {version} found in line: {l}')
      return version
  
  lg.info('No version pragma found')


class CyclomaticComplexityProcessor(Processor):
  @staticmethod
  def run(path: str) -> CyclomaticComplexityResult:
    """Given code path, return cyclomatic complexity statistics."""

    # set solc version
    version = parse_version(path)
    if version is None:
      solc_select_api.use_latest()
    else:
      solc_select_api.use_version(version)

    # gather all functions
    functions = []
    for c in Slither(path).contracts:
      functions += c.functions

    # retrieve cc for each function
    ccs = [compute_cyclomatic_complexity(f) for f in functions]

    # return statistics
    return CyclomaticComplexityResult(
      total = sum(ccs),
      mean = mean(ccs),
      median = median(ccs),
      num_functions = len(ccs),
      raw = ccs
    )


ccs1 = [1,2,3]
ccs2 = [5,2,3,5]

print( CyclomaticComplexityResult.from_ccs(ccs1) + CyclomaticComplexityResult.from_ccs(ccs2))